#!/usr/bin/python3
# Copyright 2026 Sriram
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
2.5D elevation mapper.

Fuses:
  * X/Y  - from the downward optical flow sensor (body-frame velocity,
           integrated with IMU yaw to get world position)
  * Z    - from the downward 1D lidar (altimeter)
  * obstacles - from the horizontally sweeping gimbal 2D lidar; each beam
           is projected into the world frame using the fused pose + the
           gimbal joint angle, and written into a multi-level grid that
           stores per-cell min/max obstacle height (z_min/z_max).

Outputs:
  /map                  nav_msgs/OccupancyGrid   (2D projection for planners)
  /elevation_map        drone_slam/ElevationGrid (2.5D multi-level map)
  TF  map -> base_link  (fused pose estimate)

The map frame is anchored at the drone's start pose.
"""

from __future__ import annotations

import math

from drone_slam.msg import ElevationGrid
from geometry_msgs.msg import PoseStamped, TransformStamped
from nav_msgs.msg import OccupancyGrid
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy

from tf2_ros import TransformBroadcaster

UNKNOWN, FREE, OCCUPIED = 0, 1, 2


class ElevationMapper(Node):

    def __init__(self) -> None:
        super().__init__('elevation_mapper')

        # ---- parameters -------------------------------------------------
        self.declare_parameter('resolution', 0.1)          # m/cell
        self.declare_parameter('grid_size', 240)           # cells per side
        self.declare_parameter('hit_threshold', 2)         # hits to mark occ
        self.declare_parameter('free_clearance', 0.25)     # m inflation (free ray)
        self.declare_parameter('max_range', 30.0)
        self.declare_parameter('publish_rate', 2.0)        # Hz map publishing
        self.declare_parameter('robot_radius', 0.30)       # m (for inflation)
        self.declare_parameter('sensor_height', 0.0)       # lidar z offset

        res = float(self.get_parameter('resolution').value)
        n = int(self.get_parameter('grid_size').value)
        self.res = res
        self.n = n
        self.half = n / 2.0

        # Occupancy: -1 unknown, 0 free, 100 occupied (nav_msgs convention)
        self.occ = np.full((n, n), -1, dtype=np.int8)
        # Elevation layers
        self.z_min = np.full((n, n), np.nan, dtype=np.float32)
        self.z_max = np.full((n, n), np.nan, dtype=np.float32)
        self.hits = np.zeros((n, n), dtype=np.uint32)

        # ---- fused state ------------------------------------------------
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.yaw = 0.0
        self.have_pose = False

        self._last_flow_t: float | None = None
        self._last_imu_t: float | None = None
        self._gimbal_pitch = 0.0
        self._range_z: float | None = None

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.create_subscription(
            TwistWithCovarianceStamped, '/optical_flow/velocity',
            self._on_flow, qos,
        )
        self.create_subscription(Range, '/altimeter/range', self._on_range, qos)
        self.create_subscription(Imu, '/imu/data', self._on_imu, qos)
        self.create_subscription(JointState, '/joint_states', self._on_joint, 10)
        self.create_subscription(LaserScan, '/gimbal_lidar/scan', self._on_scan, qos)

        # Map topics use transient-local durability so late joiners (RViz,
        # planners) receive the latest map immediately.
        map_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.map_pub = self.create_publisher(OccupancyGrid, '/map', map_qos)
        self.elev_pub = self.create_publisher(ElevationGrid, '/elevation_map', map_qos)
        self.pose_pub = self.create_publisher(PoseStamped, '/slam/pose', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        rate = float(self.get_parameter('publish_rate').value)
        self.create_timer(1.0 / rate, self._publish_maps)
        self.create_timer(0.05, self._publish_pose)  # 20 Hz TF/pose

        self.get_logger().info(
            f'2.5D mapper up: {n}x{n} @ {res} m ({n * res:.0f} m square)'
        )

    # ------------------------------------------------------------------ #
    # Sensor callbacks                                                    #
    # ------------------------------------------------------------------ #
    def _on_flow(self, msg: TwistWithCovarianceStamped) -> None:
        """Integrate body-frame optical flow velocity into world position."""
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        vx_b = msg.twist.twist.linear.x
        vy_b = msg.twist.twist.linear.y

        if self._last_flow_t is None:
            self._last_flow_t = t
            self.have_pose = True
            return
        dt = t - self._last_flow_t
        self._last_flow_t = t
        if dt <= 0.0 or dt > 0.5:
            return

        # Body -> world using current yaw estimate
        c, s = math.cos(self.yaw), math.sin(self.yaw)
        self.x += (c * vx_b - s * vy_b) * dt
        self.y += (s * vx_b + c * vy_b) * dt
        self.have_pose = True

    def _on_range(self, msg: Range) -> None:
        """Altimeter: distance to floor -> drone height (clamped sane)."""
        if msg.range_min <= msg.range <= msg.max_range:
            # Sensor points down: height above ground ~= measured range
            self.z = msg.range
            self._range_z = msg.range

    def _on_imu(self, msg: Imu) -> None:
        """Yaw from IMU orientation (ENU, z-up); integrates gyro as fallback."""
        q = msg.orientation
        # Validity check: a zero quaternion means "not provided"
        if abs(q.w) + abs(q.x) + abs(q.y) + abs(q.z) > 1e-6:
            siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
            self.yaw = math.atan2(siny_cosp, cosy_cosp)
            return

        # Fallback: integrate body yaw rate
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        if self._last_imu_t is not None:
            dt = t - self._last_imu_t
            if 0.0 < dt < 0.5:
                self.yaw += msg.angular_velocity.z * dt
        self._last_imu_t = t

    def _on_joint(self, msg: JointState) -> None:
        for name, pos in zip(msg.name, msg.position):
            if name == 'gimbal_pitch_joint':
                self._gimbal_pitch = pos

    # ------------------------------------------------------------------ #
    # Scan integration                                                    #
    # ------------------------------------------------------------------ #
    def _on_scan(self, msg: LaserScan) -> None:
        if not self.have_pose:
            return

        max_r = min(msg.range_max, float(self.get_parameter('max_range').value))
        sensor_z = self.z + float(self.get_parameter('sensor_height').value)

        # Drone yaw for world-frame X-Y rotation
        yaw = self.yaw
        # Gimbal pitch angle: tilts the LiDAR scan plane up/down
        pitch = self._gimbal_pitch

        for i, r in enumerate(msg.ranges):
            if not math.isfinite(r) or r < msg.range_min:
                continue
            hit = r < max_r
            rr = min(r, max_r)

            # Beam angle in body frame (azimuth from LiDAR horizontal scan)
            a_body = msg.angle_min + i * msg.angle_increment
            # Absolute world angle for X-Y projection (drone yaw + beam azimuth)
            a_world = yaw + a_body
            ca, sa = math.cos(a_world), math.sin(a_world)

            # X-Y endpoint in the map plane
            end_x = self.x + rr * ca
            end_y = self.y + rr * sa

            # Z height: drone height + range effect from pitch tilt.
            # When the pitch gimbal is at angle p, the scan plane is tilted.
            # The effective height offset for a beam at azimuth a_body is:
            #   z_offset ≈ rr * sin(pitch) * cos(a_body)
            # This accounts for the pitch tilt and the beam's direction in the
            # horizontal plane. When pitch=0, z_offset=0 (horizontal scan).
            z_offset = rr * math.sin(pitch) * math.cos(a_body)
            obst_z = sensor_z + z_offset

            if hit:
                self._mark_obstacle(end_x, end_y, obst_z)
                # Mark free space along the beam up to just before the hit
                self._raytrace_free(self.x, self.y, end_x, end_y, obst_z,
                                    clear=rr - 0.15)
            else:
                # Max-range return: everything along the beam is free
                self._raytrace_free(self.x, self.y, end_x, end_y, obst_z,
                                    clear=rr)

    def _world_to_cell(self, x: float, y: float) -> tuple[int, int] | None:
        # Map frame origin at drone start; grid centered
        ci = int(self.half + x / self.res)
        cj = int(self.half + y / self.res)
        if 0 <= ci < self.n and 0 <= cj < self.n:
            return ci, cj
        return None

    def _mark_obstacle(self, x: float, y: float, z: float) -> None:
        cell = self._world_to_cell(x, y)
        if cell is None:
            return
        i, j = cell
        self.hits[i, j] += 1
        if np.isnan(self.z_min[i, j]) or z < self.z_min[i, j]:
            self.z_min[i, j] = z
        if np.isnan(self.z_max[i, j]) or z > self.z_max[i, j]:
            self.z_max[i, j] = z
        if self.hits[i, j] >= int(self.get_parameter('hit_threshold').value):
            self.occ[i, j] = 100

    def _raytrace_free(self, x0: float, y0: float, x1: float, y1: float,
                       z: float, clear: float) -> None:
        """Bresenham-style free-space carving along a beam."""
        dist = math.hypot(x1 - x0, y1 - y0)
        if dist < 1e-6:
            return
        # Step along the beam at ~1 cell resolution
        step = self.res
        nsteps = int(min(clear, dist) / step)
        for k in range(nsteps + 1):
            d = k * step
            cell = self._world_to_cell(x0 + d * (x1 - x0) / dist,
                                       y0 + d * (y1 - y0) / dist)
            if cell is None:
                break
            i, j = cell
            if self.occ[i, j] != 100:  # never erase confirmed obstacles
                self.occ[i, j] = 0

    # ------------------------------------------------------------------ #
    # Publishing                                                          #
    # ------------------------------------------------------------------ #
    def _publish_pose(self) -> None:
        if not self.have_pose:
            return
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = self.z
        t.transform.rotation.z = math.sin(self.yaw / 2.0)
        t.transform.rotation.w = math.cos(self.yaw / 2.0)
        self.tf_broadcaster.sendTransform(t)

        p = PoseStamped()
        p.header = t.header
        p.pose.position.x = self.x
        p.pose.position.y = self.y
        p.pose.position.z = self.z
        p.pose.orientation = t.transform.rotation
        self.pose_pub.publish(p)

    def _publish_maps(self) -> None:
        stamp = self.get_clock().now().to_msg()

        # Internal arrays are indexed [x_idx, y_idx]; nav_msgs/OccupancyGrid
        # (and our ElevationGrid) are row-major with index = row(y)*w + col(x),
        # so transpose before flattening.
        occ = self.occ.T          # [y, x]
        z_min = self.z_min.T
        z_max = self.z_max.T
        hits = self.hits.T

        # --- nav_msgs/OccupancyGrid (2D projection) ---
        og = OccupancyGrid()
        og.header.stamp = stamp
        og.header.frame_id = 'map'
        og.info.resolution = self.res
        og.info.width = self.n
        og.info.height = self.n
        # Cell (0,0) sits at (-half*res, -half*res) in map frame
        og.info.origin.position.x = -self.half * self.res
        og.info.origin.position.y = -self.half * self.res
        og.info.origin.orientation.w = 1.0
        og.data = occ.flatten(order='C').tolist()
        self.map_pub.publish(og)

        # --- ElevationGrid (2.5D multi-level) ---
        eg = ElevationGrid()
        eg.header = og.header
        eg.resolution = self.res
        eg.width = self.n
        eg.height = self.n
        eg.origin = og.info.origin
        # Map occupied(100)->2, free(0)->1, unknown(-1)->0
        eg.state = np.where(occ == 100, 2,
                            np.where(occ == 0, 1, 0)).astype(np.uint8).tolist()
        eg.z_min = np.nan_to_num(z_min, nan=0.0).tolist()
        eg.z_max = np.nan_to_num(z_max, nan=0.0).tolist()
        eg.hits = hits.tolist()
        self.elev_pub.publish(eg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ElevationMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

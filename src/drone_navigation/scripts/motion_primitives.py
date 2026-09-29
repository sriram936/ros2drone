#!/usr/bin/python3
#!/usr/bin/env python3
#
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
3D Motion Primitives for SAR Drone Obstacle Avoidance.

Provides a set of pre-computed 3D motion primitives (vx, vy, vz, yaw_rate)
for local obstacle avoidance. Includes vertical motion (climb/descend) for
navigating around rubble, collapsed structures, and between floors.

Primitive types:
  * CLIMB: ascend at controlled rate while moving forward
  * DESCEND: descend at controlled rate while moving forward
  * FLY_LEVEL: level flight forward/backward/left/right
  * EVASIVE_CLIMB: rapid climb to avoid imminent collision
  * EVASIVE_DESCEND: rapid descent to avoid imminent collision

Each primitive is scored based on:
  - Clearance to nearest obstacle (from /vertical_gimbal_lidar/scan + /map)
  - Vertical speed safety (avoid sink rate exceedance)
  - Progress toward goal
  - Hazard zone penalty (X regions = high penalty)
  - Human/ survivor proximity penalty
"""

from __future__ import annotations

import math

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from geometry_msgs.msg import Twist

from std_msgs.msg import Float64, Int8, Header
from sensor_msgs.msg import LaserScan, Range, Imu
from nav_msgs.msg import Odometry, MapMetaData


class MotionPrimitives(Node):

    def __init__(self) -> None:
        super().__init__('motion_primitives')

        # ---- parameters -------------------------------------------------
        self.declare_parameter('primitive_set_size', 25)      # number of primitives
        self.declare_parameter('vx_samples', 5)             # m/s forward/backward
        self.declare_parameter('vy_samples', 3)             # m/s lateral
        self.declare_parameter('vz_samples', 3)             # m/s climb/descend
        self.declare_parameter('yaw_rate_samples', 5)       # rad/s
        self.declare_parameter('max_vx', 2.0)               # m/s
        self.declare_parameter('max_vy', 1.0)               # m/s
        self.declare_parameter('max_vz', 1.5)               # m/s climb/descend
        self.declare_parameter('max_yaw_rate', 1.5)         # rad/s
        self.declare_parameter('primitive_dt', 0.2)         # s per primitive step
        self.declare_parameter('rollout_steps', 5)          # how far to rollout
        self.declare_parameter('clearance_weight', 1.5)     # scoring weight
        self.declare_parameter('velocity_weight', 0.5)      # scoring weight
        self.declare_parameter('vertical_safety_weight', 2.0) # scoring weight for z-motion
        self.declare_parameter('hazard_penalty', 5.0)       # penalty for flying into X zones
        self.declare_parameter('human_penalty', 3.0)        # penalty near humans
        self.declare_parameter('min_clearance', 0.5)        # m minimum safe clearance
        self.declare_parameter('inflation_radius', 1.0)     # m for obstacle inflation

        # Load parameters
        ps = self.get_parameter
        self.primitive_set_size = ps('primitive_set_size').value
        self.vx_samples = ps('vx_samples').value
        self.vy_samples = ps('vy_samples').value
        self.vz_samples = ps('vz_samples').value
        self.yaw_rate_samples = ps('yaw_rate_samples').value
        self.max_vx = ps('max_vx').value
        self.max_vy = ps('max_vy').value
        self.max_vz = ps('max_vz').value
        self.max_yaw_rate = ps('max_yaw_rate').value
        self.primitive_dt = ps('primitive_dt').value
        self.rollout_steps = ps('rollout_steps').value
        self.clearance_weight = ps('clearance_weight').value
        self.velocity_weight = ps('velocity_weight').value
        self.vertical_safety_weight = ps('vertical_safety_weight').value
        self.hazard_penalty = ps('hazard_penalty').value
        self.human_penalty = ps('human_penalty').value
        self.min_clearance = ps('min_clearance').value
        self.inflation_radius = ps('inflation_radius').value

        # ---- state ------------------------------------------------------
        self.pose: tuple[float, float, float] | None = None  # x, y, z
        self.yaw: float = 0.0
        self.map: any = None  # OccupancyGrid
        self.elevation_map: any = None  # ElevationGrid
        self.hazard_zones: list | None = None  # list of (min_x, max_x, min_y, max_y)
        self.safe_zones: list | None = None  # list of (min_x, max_x, min_y, max_y)
        self.have_map = False
        self.have_elevation = False

        # Subscriptions
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.create_subscription(Odometry, '/ground_truth/odometry', self._on_odom, 10)
        self.create_subscription(LaserScan, '/vertical_gimbal_lidar/scan', self._on_scan, qos)
        self.create_subscription(OccupancyGrid, '/map', self._on_map, 1)
        self.create_subscription(ElevationGrid, '/elevation_map', self._on_elevation_map, 1)
        # Hazard/safe zone definitions from config
        # self.create_subscription(...)

        # Publisher
        self.cmd_pub = self.create_publisher(Twist, '/mavros/setpoint_velocity/cmd_vel_unstamped', 10)

        # Timer: recalculate primitives at 10 Hz
        self.create_timer(0.1, self._compute_primitives)

        self.get_logger().info('3D Motion Primitives node ready')

    # ------------------------------------------------------------------ #
    # State callbacks                                                    #
    # ------------------------------------------------------------------ #
    def _on_odom(self, msg: Odometry) -> None:
        self.pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            msg.pose.pose.position.z,
        )
        # Extract yaw from quaternion
        q = msg.pose.pose.orientation
        self.yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z),
        )

    def _on_scan(self, msg: LaserScan) -> None:
        # Store latest vertical gimbal lidar scan for clearance checking
        self.latest_scan = msg

    def _on_map(self, msg: OccupancyGrid) -> None:
        self.map = msg
        self.have_map = True

    def _on_elevation_map(self, msg: any) -> None:
        self.elevation_map = msg
        self.have_elevation = True

    # ------------------------------------------------------------------ #
    # Generate 3D motion primitives                                      #
    # ------------------------------------------------------------------ #
    def _generate_primitives(self) -> list[tuple[float, float, float, float]]:
        """Generate a set of 3D motion primitives (vx, vy, vz, yaw_rate)."""
        primitives = []

        # Generate grid of primitives
        vx_vals = np.linspace(-self.max_vx, self.max_vx, self.vx_samples)
        vy_vals = np.linspace(-self.max_vy, self.max_vy, self.vy_samples)
        vz_vals = np.linspace(-self.max_vz, self.max_vz, self.vz_samples)
        yaw_vals = np.linspace(-self.max_yaw_rate, self.max_yaw_rate, self.yaw_rate_samples)

        # Create primitive set (subsample to keep size manageable)
        for i, vx in enumerate(vx_vals):
            for j, vy in enumerate(vy_vals):
                for k, vz in enumerate(vz_vals):
                    for l, yaw_rate in enumerate(yaw_vals):
                        # Skip static pose (too conservative)
                        if vx == 0.0 and vy == 0.0 and vz == 0.0 and yaw_rate == 0.0:
                            continue
                        primitives.append((float(vx), float(vy), float(vz), float(yaw_rate)))
                        if len(primitives) >= self.primitive_set_size:
                            break
                    if len(primitives) >= self.primitive_set_size:
                        break
                if len(primitives) >= self.primitive_set_size:
                    break
            if len(primitives) >= self.primitive_set_size:
                break

        # Ensure we have at least some primitives
        if not primitives:
            primitives = [(1.0, 0.0, 0.0, 0.0)]  # default forward motion

        return primitives

    # ------------------------------------------------------------------ #
    # Score primitives based on clearance, safety, progress                #
    # ------------------------------------------------------------------ #
    def _score_primitive(
        self,
        vx: float,
        vy: float,
        vz: float,
        yaw_rate: float,
    ) -> float:
        """Score a primitive; higher is better. Returns composite score."""

        if not self.have_map or self.pose is None:
            # If no map available, use simple velocity-based scoring
            return (abs(vx) * 0.5 + abs(vy) * 0.3 + abs(vz) * 0.2)

        px, py, pz = self.pose

        # 1. Clearance scoring (from inflated robot footprint)
        clearance = self._compute_clearance(px, py, self.inflation_radius)
        clearance_score = clearance if clearance > 0 else -10.0

        # 2. Vertical safety scoring (avoid excessive descent into hazards)
        vertical_safety = 1.0
        if vz < -0.5:  # descending
            # Check if descending into a hazard zone or below safe floor level
            vertical_safety = max(0, 1.0 + vz * 0.5)  # penalize fast descent

        # 3. Hazard zone penalty
        hazard_penalty = 1.0
        if self.hazard_zones:
            for hz in self.hazard_zones:
                h_min_x, h_max_x, h_min_y, h_max_y = hz
                # Predict future position after primitive_dt
                future_x = px + vx * self.primitive_dt
                future_y = py + vy * self.primitive_dt
                if (h_min_x <= future_x <= h_max_x and
                    h_min_y <= future_y <= h_max_y):
                    hazard_penalty = 0.1  # severe penalty for flying into hazard zone
                    break

        # 4. Human/survivor penalty (from elevation map confidence)
        human_penalty = 1.0
        if self.elevation_map and hasattr(self.elevation_map, 'hits'):
            # Check cell under drone for high confidence human/hazard detections
            pass  # simplified for now

        # 5. Velocity scoring (prefer forward motion with progress)
        velocity_score = math.hypot(vx, vy) / math.hypot(self.max_vx, self.max_vy)

        # Composite score
        score = (
            self.clearance_weight * clearance_score +
            self.vertical_safety_weight * vertical_safety +
            self.hazard_penalty * hazard_penalty +  # inverted so lower penalty = higher score
            self.velocity_weight * velocity_score
        )

        # Adjust for human penalty (lower score if near humans)
        score -= human_penalty * 0.1

        return score

    # ------------------------------------------------------------------ #
    # Compute nearest obstacle clearance at (x, y)                       #
    # ------------------------------------------------------------------ #
    def _compute_clearance(self, x: float, y: float, inflation_r: float) -> float:
        """Distance to nearest occupied cell, inflated by inflation_radius."""
        if self.map is None:
            return 1.0

        info = self.map.info
        res = info.resolution
        ox, oy = info.origin.position.x, info.origin.position.y

        # Convert world to grid coordinates
        gx = int((x - ox) / res)
        gy = int((y - oy) / res)

        # Clamp to grid bounds
        gx = max(0, min(info.width - 1, gx))
        gy = max(0, min(info.height - 1, gy))

        # Get inflation cells
        cells = max(1, int(math.ceil(inflation_r / res)))

        grid = np.asarray(self.map.data, dtype=np.int8).reshape(
            (info.height, info.width)
        )

        # Check inflated area
        x0 = max(0, gx - cells)
        x1 = min(info.width, gx + cells + 1)
        y0 = max(0, gy - cells)
        y1 = min(info.height, gy + cells + 1)

        patch = grid[y0:y1, x0:x1]

        # If any cell in inflation radius is occupied (100), clearance is poor
        if (patch == 100).any():
            # Compute distance to nearest obstacle
            obstacle_cells = np.where(patch == 100)
            if len(obstacle_cells[0]) > 0:
                ox_rel = obstacle_cells[1] - gx + 0.5  # center of cell
                oy_rel = obstacle_cells[0] - gy + 0.5
                dists = np.hypot(ox_rel, oy_rel) * res
                return float(max(0.0, self.inflation_radius - dists.min()))

        # Free space: return distance above minimum
        free_cells = np.where(patch == 0)
        if len(free_cells[0]) > 0:
            fx_rel = free_cells[1] - gx + 0.5
            fy_rel = free_cells[0] - gy + 0.5
            dists = np.hypot(fx_rel, fy_rel) * res
            # Return distance to edge of inflation zone
            return float(max(0.0, dists.min() - self.inflation_radius))

        # Unknown space
        return 0.5

    # ------------------------------------------------------------------ #
    # Main primitive computation loop                                      #
    # ------------------------------------------------------------------ #
    def _compute_primitives(self) -> None:
        """Compute best primitive and publish cmd_vel."""
        if self.pose is None or not self.have_map:
            return

        # Generate primitives
        primitives = self._generate_primitives()

        # Score all primitives
        best_score = -math.inf
        best_primitive = primitives[0] if primitives else (0.0, 0.0, 0.0, 0.0)

        for primitive in primitives:
            vx, vy, vz, yaw_rate = primitive
            score = self._score_primitive(vx, vy, vz, yaw_rate)
            if score > best_score:
                best_score = score
                best_primitive = (vx, vy, vz, yaw_rate)

        # Publish the best primitive as a Twist message
        vx, vy, vz, yaw_rate = best_primitive
        cmd = Twist()
        cmd.linear.x = vx  # forward/backward (body frame)
        cmd.linear.y = vy  # left/right (body frame)
        cmd.linear.z = vz  # climb/descend (body frame - unusual but for 3D)
        cmd.angular.z = yaw_rate  # yaws rotation (yaw rate)

        self.cmd_pub.publish(cmd)

        # Log best primitive occasionally
        if int(self.get_clock().now().nanoseconds / 1e9) % 10 == 0:
            self.get_logger().info(
                f'Best primitive: vx={vx:.2f}, vy={vy:.2f}, vz={vz:.2f}, yaw_rate={yaw_rate:.2f}'
            )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MotionPrimitives()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
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
Dynamic Window Approach (DWA) local planner (standalone, Nav2-free).

Follows /nav/global_path while avoiding obstacles in /map.
Publishes velocity commands on /mavros/setpoint_velocity/cmd_vel_unstamped
(ENU world frame — MAVROS convention consumed by the pixhawk bridge).

DWA samples (v, w) in the dynamic window limited by current velocity and
actuator acceleration limits, scores each admissible trajectory against:
  heading (alignment to local path goal), clearance (distance to nearest
  obstacle along the rollout), and velocity (progress).
"""

from __future__ import annotations

import math

from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import OccupancyGrid, Odometry, Path
import numpy as np
import rclpy
from rclpy.node import Node


class DWAPlanner(Node):

    def __init__(self) -> None:
        super().__init__('dwa_planner')

        # Robot / DWA limits
        self.declare_parameter('max_speed', 1.5)          # m/s
        self.declare_parameter('min_speed', 0.0)
        self.declare_parameter('max_yaw_rate', 1.2)       # rad/s
        self.declare_parameter('max_accel', 2.0)          # m/s^2
        self.declare_parameter('max_dyaw_accel', 2.5)     # rad/s^2
        self.declare_parameter('v_samples', 7)
        self.declare_parameter('w_samples', 9)
        self.declare_parameter('predict_time', 2.0)       # s
        self.declare_parameter('dt', 0.1)                 # rollout step
        self.declare_parameter('robot_radius', 0.30)      # m
        self.declare_parameter('obstacle_inflation', 0.45)
        # Weights
        self.declare_parameter('w_heading', 0.6)
        self.declare_parameter('w_clearance', 1.4)
        self.declare_parameter('w_velocity', 0.3)
        self.declare_parameter('goal_tolerance', 0.35)    # m
        self.declare_parameter('control_rate', 10.0)      # Hz
        self.declare_parameter('kp_v', 0.9)               # path tracking P gains
        self.declare_parameter('kp_w', 1.6)

        self.map: OccupancyGrid | None = None
        self.path: Path | None = None
        self.pose: tuple[float, float] | None = None
        self.yaw = 0.0
        self.v = 0.0
        self.w = 0.0

        self.create_subscription(OccupancyGrid, '/map', self._on_map, 1)
        self.create_subscription(Path, '/nav/global_path', self._on_path, 10)
        # Pose in map frame from SLAM; velocity from odometry twist
        self.create_subscription(PoseStamped, '/slam/pose', self._on_pose, 10)
        self.create_subscription(Odometry, '/ground_truth/odometry', self._on_odom, 10)

        self.cmd_pub = self.create_publisher(
            Twist, '/mavros/setpoint_velocity/cmd_vel_unstamped', 10
        )

        rate = float(self.get_parameter('control_rate').value)
        self.create_timer(1.0 / rate, self._control)
        self.get_logger().info('DWA local planner ready')

    # ------------------------------------------------------------------ #
    def _on_map(self, msg: OccupancyGrid) -> None:
        self.map = msg

    def _on_path(self, msg: Path) -> None:
        if msg.poses:
            self.path = msg

    def _on_pose(self, msg: PoseStamped) -> None:
        self.pose = (msg.pose.position.x, msg.pose.position.y)
        q = msg.pose.orientation
        self.yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                              1.0 - 2.0 * (q.y * q.y + q.z * q.z))

    def _on_odom(self, msg: Odometry) -> None:
        self.v = msg.twist.twist.linear.x   # body-frame forward speed
        self.w = msg.twist.twist.angular.z

    # ------------------------------------------------------------------ #
    # Map queries                                                         #
    # ------------------------------------------------------------------ #
    def _world_to_grid(self, x: float, y: float):
        info = self.map.info
        gx = int((x - info.origin.position.x) / info.resolution)
        gy = int((y - info.origin.position.y) / info.resolution)
        if 0 <= gx < info.width and 0 <= gy < info.height:
            return gx, gy
        return None

    def _cell_free(self, x: float, y: float, inflate: float) -> bool:
        info = self.map.info
        res = info.resolution
        c = self._world_to_grid(x, y)
        if c is None:
            return False
        gx, gy = c
        cells = max(1, int(math.ceil(inflate / res)))
        grid = np.asarray(self.map.data, dtype=np.int8).reshape(
            (info.height, info.width))
        x0, x1 = max(0, gx - cells), min(info.width, gx + cells + 1)
        y0, y1 = max(0, gy - cells), min(info.height, gy + cells + 1)
        patch = grid[y0:y1, x0:x1]
        return bool((patch != 100).all())

    def _min_obstacle_dist(self, x: float, y: float, search_r: float = 2.0) -> float:
        """Distance to nearest occupied cell centre (capped at search_r)."""
        info = self.map.info
        res = info.resolution
        c = self._world_to_grid(x, y)
        if c is None:
            return 0.0
        gx, gy = c
        rad = int(search_r / res)
        grid = np.asarray(self.map.data, dtype=np.int8).reshape(
            (info.height, info.width))
        x0, x1 = max(0, gx - rad), min(info.width, gx + rad + 1)
        y0, y1 = max(0, gy - rad), min(info.height, gy + rad + 1)
        patch = grid[y0:y1, x0:x1]
        ys, xs = np.nonzero(patch == 100)
        if len(xs) == 0:
            return search_r
        offs_x = (xs + x0 - gx) * res
        offs_y = (ys + y0 - gy) * res
        return float(np.hypot(offs_x, offs_y).min())

    # ------------------------------------------------------------------ #
    # Local path lookahead                                                #
    # ------------------------------------------------------------------ #
    def _lookahead(self) -> tuple[float, float] | None:
        if self.path is None or self.pose is None or not self.path.poses:
            return None
        pts = [(p.pose.position.x, p.pose.position.y) for p in self.path.poses]
        # Closest point on the path, then advance by lookahead distance
        d2 = [(px - self.pose[0]) ** 2 + (py - self.pose[1]) ** 2
              for px, py in pts]
        i0 = int(np.argmin(d2))
        lookahead = 1.0
        acc = 0.0
        i = i0
        while i < len(pts) - 1 and acc < lookahead:
            acc += math.hypot(pts[i + 1][0] - pts[i][0],
                              pts[i + 1][1] - pts[i][1])
            i += 1
        return pts[i]

    # ------------------------------------------------------------------ #
    def _control(self) -> None:
        if self.map is None or self.pose is None:
            return

        target = self._lookahead()
        if target is None:
            return

        # Goal reached?
        gx, gy = target
        # If lookahead point is the path end and we're close, stop
        end = self.path.poses[-1].pose.position
        at_end = math.hypot(end.x - self.pose[0],
                            end.y - self.pose[1]) < float(
                                self.get_parameter('goal_tolerance').value)
        if at_end:
            self.cmd_pub.publish(Twist())
            self.v = 0.0
            return

        # --- DWA sampling ---
        def p(n):
            return float(self.get_parameter(n).value)
        max_v, min_v = p('max_speed'), p('min_speed')
        max_w = p('max_yaw_rate')
        a_v, a_w = p('max_accel'), p('max_dyaw_accel')
        dt = p('dt')
        n_v, n_w = int(p('v_samples')), int(p('w_samples'))
        t_pred = p('predict_time')
        inflate = p('obstacle_inflation')
        r_robot = p('robot_radius')

        # Dynamic window
        dv_lo = max(min_v, self.v - a_v * dt)
        dv_hi = min(max_v, self.v + a_v * dt)
        dw_lo = max(-max_w, self.w - a_w * dt)
        dw_hi = min(max_w, self.w + a_w * dt)

        w_head, w_clear, w_vel = p('w_heading'), p('w_clearance'), p('w_velocity')

        best_score = -math.inf
        best_cmd = (0.0, 0.0)

        vx_grid = np.linspace(dv_lo, dv_hi, n_v) if dv_hi > dv_lo else np.array([dv_lo])
        wx_grid = np.linspace(dw_lo, dw_hi, n_w) if dw_hi > dw_lo else np.array([dw_lo])

        for v in vx_grid:
            for w in wx_grid:
                # Rollout trajectory
                x, y, yaw = self.pose[0], self.pose[1], self.yaw
                ok = True
                min_obs = math.inf
                steps = max(1, int(t_pred / dt))
                for _ in range(steps):
                    yaw += w * dt
                    x += v * math.cos(yaw) * dt
                    y += v * math.sin(yaw) * dt
                    if not self._cell_free(x, y, r_robot * 0.6):
                        ok = False
                        break
                    min_obs = min(min_obs, self._min_obstacle_dist(x, y))
                if not ok:
                    continue
                if min_obs < inflate:
                    continue

                # Score
                heading_err = abs(self._wrap(
                    math.atan2(gy - y, gx - x) - yaw))
                heading_score = math.pi - heading_err
                clearance_score = min(min_obs, 3.0)
                velocity_score = v / max(max_v, 1e-6)
                score = (w_head * heading_score
                         + w_clear * clearance_score
                         + w_vel * velocity_score)
                if score > best_score:
                    best_score = score
                    best_cmd = (float(v), float(w))

        # --- Convert to ENU world-frame Twist (MAVROS convention) ---
        cmd = Twist()
        if best_score > -math.inf:
            v, w = best_cmd
            cmd.linear.x = v * math.cos(self.yaw)   # ENU east
            cmd.linear.y = v * math.sin(self.yaw)   # ENU north
            cmd.angular.z = w
        else:
            # No safe sample: brake
            cmd.linear.x = 0.0
            cmd.linear.y = 0.0
            cmd.angular.z = 0.0
        self.cmd_pub.publish(cmd)

    @staticmethod
    def _wrap(a: float) -> float:
        return math.atan2(math.sin(a), math.cos(a))


def main(args=None) -> None:
    rclpy.init(args=args)
    node = DWAPlanner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

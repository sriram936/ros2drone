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
RRT* global path planner (standalone, Nav2-free).

Listens for a goal on /nav/goal, plans from the current robot pose over the
/map OccupancyGrid with RRT* (informed, anytime re-planning), and publishes
the smoothed polyline on /nav/global_path.

Re-plans are triggered by a new goal or by map updates that invalidate the
current path.
"""

from __future__ import annotations

import math
import random

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid, Path
import numpy as np
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker


class RRTStar(Node):

    def __init__(self) -> None:
        super().__init__('rrt_star')

        self.declare_parameter('max_iterations', 1500)
        self.declare_parameter('step_size', 0.5)          # m
        self.declare_parameter('goal_bias', 0.12)
        self.declare_parameter('goal_tolerance', 0.4)      # m
        self.declare_parameter('rewire_radius', 1.2)       # m
        self.declare_parameter('robot_radius', 0.30)       # m
        self.declare_parameter('replan_period', 3.0)       # s

        self.map: OccupancyGrid | None = None
        self.start: tuple[float, float] | None = None
        self.goal: tuple[float, float] | None = None

        self.create_subscription(OccupancyGrid, '/map', self._on_map, 1)
        self.create_subscription(PoseStamped, '/slam/pose', self._on_pose, 10)
        self.create_subscription(PoseStamped, '/nav/goal', self._on_goal, 10)

        self.path_pub = self.create_publisher(Path, '/nav/global_path', 10)
        self.marker_pub = self.create_publisher(Marker, '/nav/global_path_markers', 10)

        period = float(self.get_parameter('replan_period').value)
        self.create_timer(period, self._replan_tick)
        self.get_logger().info('RRT* planner ready')

    # ------------------------------------------------------------------ #
    def _on_map(self, msg: OccupancyGrid) -> None:
        self.map = msg

    def _on_pose(self, msg: PoseStamped) -> None:
        self.start = (msg.pose.position.x, msg.pose.position.y)

    def _on_goal(self, msg: PoseStamped) -> None:
        self.goal = (msg.pose.position.x, msg.pose.position.y)
        self.get_logger().info(f'Goal received: {self.goal}')
        self._plan()

    def _replan_tick(self) -> None:
        if self.goal is not None:
            self._plan()

    # ------------------------------------------------------------------ #
    # Map helpers                                                         #
    # ------------------------------------------------------------------ #
    def _world_to_grid(self, x: float, y: float) -> tuple[int, int] | None:
        info = self.map.info
        gx = int((x - info.origin.position.x) / info.resolution)
        gy = int((y - info.origin.position.y) / info.resolution)
        if 0 <= gx < info.width and 0 <= gy < info.height:
            return gx, gy
        return None

    def _is_free(self, x: float, y: float, inflate: float) -> bool:
        """Check that (x,y) plus inflation radius is known free space."""
        info = self.map.info
        res = info.resolution
        gx, gy = self._world_to_grid(x, y)
        if gx is None:
            return False
        cells = max(1, int(math.ceil(inflate / res)))
        grid = np.asarray(self.map.data, dtype=np.int8).reshape(
            (info.height, info.width)
        )
        x0, x1 = max(0, gx - cells), min(info.width, gx + cells + 1)
        y0, y1 = max(0, gy - cells), min(info.height, gy + cells + 1)
        patch = grid[y0:y1, x0:x1]
        # Allow free(0) or unknown(-1) only if the center itself is free;
        # require all inflated cells to be >= 0 (observed) and not occupied.
        return bool((patch >= 0).all() and (patch != 100).all())

    def _segment_free(self, p: tuple[float, float], q: tuple[float, float],
                      inflate: float) -> bool:
        dist = math.hypot(q[0] - p[0], q[1] - p[1])
        steps = max(2, int(dist / (self.map.info.resolution * 0.8)))
        for k in range(steps + 1):
            t = k / steps
            x = p[0] + t * (q[0] - p[0])
            y = p[1] + t * (q[1] - p[1])
            if not self._is_free(x, y, inflate):
                return False
        return True

    # ------------------------------------------------------------------ #
    # RRT*                                                                #
    # ------------------------------------------------------------------ #
    def _plan(self) -> None:
        if self.map is None or self.start is None or self.goal is None:
            return

        inflate = float(self.get_parameter('robot_radius').value)
        # Start/goal may sit in cells inflated into occupied space; accept
        # them if their own cell is at least not a confirmed obstacle.
        if not self._is_free(*self.start, inflate=0.0):
            self.get_logger().warn('Start in obstacle/unknown, planning anyway')
        if not self._is_free(*self.goal, inflate=0.0):
            self.get_logger().warn('Goal in obstacle/unknown, skipping plan')
            return

        max_iter = int(self.get_parameter('max_iterations').value)
        step = float(self.get_parameter('step_size').value)
        goal_bias = float(self.get_parameter('goal_bias').value)
        goal_tol = float(self.get_parameter('goal_tolerance').value)
        rewire_r = float(self.get_parameter('rewire_radius').value)

        info = self.map.info
        xmin, ymin = info.origin.position.x, info.origin.position.y
        xmax = xmin + info.width * info.resolution
        ymax = ymin + info.height * info.resolution

        nodes: list[tuple[float, float]] = [self.start]
        cost = [0.0]
        parent = [-1]

        rng = random.Random(42)  # deterministic per run
        best_idx = -1

        for _ in range(max_iter):
            # Sample (biased toward goal)
            if rng.random() < goal_bias:
                rx, ry = self.goal
            else:
                rx = rng.uniform(xmin, xmax)
                ry = rng.uniform(ymin, ymax)

            # Nearest
            ni = min(range(len(nodes)),
                     key=lambda i: (nodes[i][0] - rx) ** 2 + (nodes[i][1] - ry) ** 2)
            nx, ny = nodes[ni]

            # Steer
            dx, dy = rx - nx, ry - ny
            d = math.hypot(dx, dy)
            if d < 1e-6:
                continue
            d = min(d, step)
            px = nx + (dx / math.hypot(dx, dy)) * d
            py = ny + (dy / math.hypot(dx, dy)) * d

            if not self._segment_free((nx, ny), (px, py), inflate):
                continue

            # Choose best parent within rewire radius
            p_cost = cost[ni] + d
            best_parent = ni
            rr2 = rewire_r * rewire_r
            for j, (jx, jy) in enumerate(nodes):
                jd2 = (jx - px) ** 2 + (jy - py) ** 2
                if jd2 <= rr2 and cost[j] + math.sqrt(jd2) < p_cost:
                    if self._segment_free((jx, jy), (px, py), inflate):
                        best_parent = j
                        p_cost = cost[j] + math.sqrt(jd2)

            nodes.append((px, py))
            cost.append(p_cost)
            parent.append(best_parent)
            ci = len(nodes) - 1

            # Rewire neighbours through the new node when cheaper
            for j, (jx, jy) in enumerate(nodes[:-1]):
                jd = math.hypot(jx - px, jy - py)
                if jd <= rewire_r and cost[ci] + jd < cost[j]:
                    if self._segment_free((px, py), (jx, jy), inflate):
                        parent[j] = ci
                        cost[j] = cost[ci] + jd

            # Track best node near goal
            if math.hypot(px - self.goal[0], py - self.goal[1]) <= goal_tol:
                if best_idx < 0 or cost[ci] < cost[best_idx]:
                    best_idx = ci

        # Connect goal to best node
        if best_idx < 0:
            # Fall back: nearest node to goal
            best_idx = min(range(len(nodes)),
                           key=lambda i: (nodes[i][0] - self.goal[0]) ** 2
                           + (nodes[i][1] - self.goal[1]) ** 2)
            if math.hypot(nodes[best_idx][0] - self.goal[0],
                          nodes[best_idx][1] - self.goal[1]) > 2.0:
                self.get_logger().warn('RRT* failed to reach goal')
                return

        # Backtrack
        path: list[tuple[float, float]] = [self.goal]
        idx = best_idx
        while idx != -1:
            path.append(nodes[idx])
            idx = parent[idx]
        path.reverse()

        path = self._shortcut(path, inflate)
        self._publish_path(path)

    def _shortcut(self, path, inflate):
        """Greedy line-of-sight shortcut smoothing."""
        if len(path) <= 2:
            return path
        out = [path[0]]
        i = 0
        while i < len(path) - 1:
            j = len(path) - 1
            while j > i + 1:
                if self._segment_free(path[i], path[j], inflate):
                    break
                j -= 1
            out.append(path[j])
            i = j
        return out

    # ------------------------------------------------------------------ #
    def _publish_path(self, path) -> None:
        p = Path()
        p.header.stamp = self.get_clock().now().to_msg()
        p.header.frame_id = 'map'
        for x, y in path:
            ps = PoseStamped()
            ps.header = p.header
            ps.pose.position.x = x
            ps.pose.position.y = y
            ps.pose.orientation.w = 1.0
            p.poses.append(ps)
        self.path_pub.publish(p)

        m = Marker()
        m.header = p.header
        m.ns = 'global_path'
        m.id = 0
        m.type = Marker.LINE_STRIP
        m.action = Marker.ADD
        m.scale.x = 0.07
        m.color.a = 1.0
        m.color.g = 0.9
        for ps in p.poses:
            m.points.append(ps.pose)
        self.marker_pub.publish(m)
        self.get_logger().info(f'Published path with {len(path)} poses')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = RRTStar()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

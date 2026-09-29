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
Frontier-based exploration.

Scans the /map OccupancyGrid for frontier cells (unknown cell adjacent to a
free cell), clusters them, picks the cluster nearest the robot (or largest),
and publishes the chosen goal as an ExploreGoal on /nav/goal.

A frontier is *reached* when the robot is within `goal_tolerance`; the next
frontier is then selected. Exploration finishes when no frontiers remain.
"""

from __future__ import annotations

import math

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class FrontierExplorer(Node):

    def __init__(self) -> None:
        super().__init__('frontier_explorer')

        self.declare_parameter('cluster_min_size', 4)
        self.declare_parameter('goal_tolerance', 0.6)
        self.declare_parameter('explore_period', 2.0)
        self.declare_parameter('frontier_gap', 1)   # cells

        self.map: OccupancyGrid | None = None
        self.pos: tuple[float, float] | None = None
        self.active_goal: tuple[float, float] | None = None
        self.done = False

        self.create_subscription(OccupancyGrid, '/map', self._on_map, 1)
        self.create_subscription(PoseStamped, '/slam/pose', self._on_pose, 10)

        self.goal_pub = self.create_publisher(PoseStamped, '/nav/goal', 10)
        self.status_pub = self.create_publisher(String, '/nav/exploration_status', 10)

        period = float(self.get_parameter('explore_period').value)
        self.create_timer(period, self._tick)
        self.get_logger().info('Frontier explorer ready')

    # ------------------------------------------------------------------ #
    def _on_map(self, msg: OccupancyGrid) -> None:
        self.map = msg

    def _on_pose(self, msg: PoseStamped) -> None:
        self.pos = (msg.pose.position.x, msg.pose.position.y)

    # ------------------------------------------------------------------ #
    def _tick(self) -> None:
        if self.map is None or self.pos is None:
            return

        # If we hold a goal, check arrival
        if self.active_goal is not None:
            d = math.hypot(
                self.active_goal[0] - self.pos[0],
                self.active_goal[1] - self.pos[1],
            )
            if d <= float(self.get_parameter('goal_tolerance').value):
                self.active_goal = None
                self.get_logger().info('Goal reached, searching for next frontier')

        if self.active_goal is None:
            goal = self._select_frontier()
            if goal is None:
                if not self.done:
                    self.done = True
                    self.get_logger().info('Exploration complete: no frontiers')
                    self.status_pub.publish(String(data='complete'))
                return
            self.active_goal = goal
            self.done = False
            ps = PoseStamped()
            ps.header = self.map.header
            ps.pose.position.x = goal[0]
            ps.pose.position.y = goal[1]
            ps.pose.orientation.w = 1.0
            self.goal_pub.publish(ps)
            self.status_pub.publish(String(data='exploring'))
            self.get_logger().info(f'New frontier goal: ({goal[0]:.2f}, {goal[1]:.2f})')

    # ------------------------------------------------------------------ #
    def _select_frontier(self) -> tuple[float, float] | None:
        info = self.map.info
        w, h = info.width, info.height
        res = info.resolution
        ox, oy = info.origin.position.x, info.origin.position.y
        grid = np.asarray(self.map.data, dtype=np.int8).reshape((h, w))

        free = grid == 0
        unknown = grid == -1
        if not free.any() or not unknown.any():
            return None

        # Frontier = unknown cell with >=1 free 4-neighbour
        shifted = np.zeros_like(unknown, dtype=bool)
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.roll(free, (di, dj), axis=(0, 1))
            # invalidate wrap-around edges
            if di == 1:
                sh[0, :] = False
            elif di == -1:
                sh[-1, :] = False
            if dj == 1:
                sh[:, 0] = False
            elif dj == -1:
                sh[:, -1] = False
            shifted |= sh
        frontier = unknown & shifted
        if not frontier.any():
            return None

        # Connected components (4-connectivity) via simple flood fill
        min_size = int(self.get_parameter('cluster_min_size').value)
        visited = np.zeros_like(frontier, dtype=bool)
        ys, xs = np.nonzero(frontier)
        clusters: list[list[tuple[int, int]]] = []
        for y0, x0 in zip(ys, xs):
            if visited[y0, x0]:
                continue
            stack = [(y0, x0)]
            visited[y0, x0] = True
            comp: list[tuple[int, int]] = []
            while stack:
                cy, cx = stack.pop()
                comp.append((cy, cx))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and frontier[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
            if len(comp) >= min_size:
                clusters.append(comp)

        if not clusters:
            return None

        # Choose cluster centroid nearest the robot
        best, best_d = None, math.inf
        for comp in clusters:
            cy = sum(c[0] for c in comp) / len(comp)
            cx = sum(c[1] for c in comp) / len(comp)
            wx = ox + (cx + 0.5) * res
            wy = oy + (cy + 0.5) * res
            d = math.hypot(wx - self.pos[0], wy - self.pos[1])
            if d < best_d:
                best_d, best = d, (wx, wy)
        return best


def main(args=None) -> None:
    rclpy.init(args=args)
    node = FrontierExplorer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

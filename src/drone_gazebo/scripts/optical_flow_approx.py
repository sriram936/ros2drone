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
Downward optical flow approximation.

gz-sim has no native optical-flow sensor, so this node emulates one:
it consumes ground-truth odometry, converts the planar velocity into the
drone body frame (what a downward optical flow chip would report over
textureless-to-textured ground), and adds Gaussian noise + slow bias walk
to mimic drift.

Publishes:
  /optical_flow/velocity  geometry_msgs/TwistWithCovarianceStamped
      linear.x  -> body-frame surface velocity vx (m/s)
      linear.y  -> body-frame surface velocity vy (m/s)
      linear.z  -> surface texture quality (1.0 = good, 0 = lost)
"""

from __future__ import annotations

import math

from geometry_msgs.msg import TwistWithCovarianceStamped
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy


class OpticalFlowApprox(Node):

    def __init__(self) -> None:
        super().__init__('optical_flow_approx')

        self.declare_parameter('update_rate', 50.0)
        self.declare_parameter('noise_stddev', 0.05)       # m/s
        self.declare_parameter('bias_walk_stddev', 0.001)  # m/s per sqrt(s)
        self.declare_parameter('max_flow_vel', 10.0)       # m/s saturation

        self.noise_stddev = float(self.get_parameter('noise_stddev').value)
        self.bias_walk = float(self.get_parameter('bias_walk_stddev').value)
        self.max_vel = float(self.get_parameter('max_flow_vel').value)

        self._bias_x = 0.0
        self._bias_y = 0.0
        self._last_time: float | None = None
        self._last_pose: tuple[float, float] | None = None

        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.pub = self.create_publisher(
            TwistWithCovarianceStamped, '/optical_flow/velocity', sensor_qos
        )
        self.sub = self.create_subscription(
            Odometry, '/ground_truth/odometry', self._on_odom, sensor_qos
        )

        rate = float(self.get_parameter('update_rate').value)
        self.create_timer(1.0 / rate, self._tick)
        self._pending: Odometry | None = None
        self.get_logger().info('Optical flow approximation running')

    def _on_odom(self, msg: Odometry) -> None:
        self._pending = msg

    def _tick(self) -> None:
        msg = self._pending
        if msg is None:
            return

        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        x, y = msg.pose.pose.position.x, msg.pose.pose.position.y

        # First sample: seed state, no velocity yet.
        if self._last_time is None or self._last_pose is None:
            self._last_time, self._last_pose = t, (x, y)
            return

        dt = t - self._last_time
        if dt <= 1e-6 or dt > 0.5:  # gap / sim reset -> reseed
            self._last_time, self._last_pose = t, (x, y)
            return

        # World-frame planar velocity from finite difference
        vx_w = (x - self._last_pose[0]) / dt
        vy_w = (y - self._last_pose[1]) / dt

        # Yaw from odometry quaternion (ENU, z-up)
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        # Rotate world velocity into body frame (what the flow chip sees)
        c, s = math.cos(yaw), math.sin(yaw)
        vx_b = c * vx_w + s * vy_w
        vy_b = -s * vx_w + c * vy_w

        # Random-walk bias + white noise
        self._bias_x += self.bias_walk * math.sqrt(dt) * self._gauss()
        self._bias_y += self.bias_walk * math.sqrt(dt) * self._gauss()
        vx_b += self._bias_x + self.noise_stddev * self._gauss()
        vy_b += self._bias_y + self.noise_stddev * self._gauss()

        # Saturate like a real flow sensor
        vx_b = max(-self.max_vel, min(self.max_vel, vx_b))
        vy_b = max(-self.max_vel, min(self.max_vel, vy_b))

        out = TwistWithCovarianceStamped()
        out.header.stamp = msg.header.stamp
        out.header.frame_id = 'optical_flow_link'
        out.twist.twist.linear.x = vx_b
        out.twist.twist.linear.y = vy_b
        out.twist.twist.linear.z = 1.0  # texture quality proxy
        # Covariance: xy = noise^2, z (quality) = small
        out.twist.covariance[0] = self.noise_stddev**2
        out.twist.covariance[7] = self.noise_stddev**2
        out.twist.covariance[14] = 0.01
        self.pub.publish(out)

        self._last_time, self._last_pose = t, (x, y)

    @staticmethod
    def _gauss() -> float:
        import random
        return random.gauss(0.0, 1.0)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = OpticalFlowApprox()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

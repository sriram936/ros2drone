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
3D Gimbal controller with sweep + focus for SAR drone.
Behaviour (per spec):
  * NORMAL mode : yaw-sweep the gimbal continuously between +45 deg and -45 deg
                  at 0.5 rad/s (triangle wave), pitch holds 0 (horizontal),
                  roll holds 0 (level).
  * FOCUS mode  : when the 2D lidar detects an obstacle closer than
                  `obstacle_threshold` whose body-frame bearing lies inside
                  the +/-15 deg window around the drone's forward direction,
                  immediately clamp yaw to +/-15 deg and speed up to 2.0 rad/s.
                  Pitch clamps to +/-15 deg elevation to focus on obstacle.
                  Roll clamps to 0 (keep level).
  * FOCUS is held until no in-window obstacle is seen for `focus_timeout`
                  seconds, then NORMAL resumes.

Interfaces:
  subscribes : /vertical_gimbal_lidar/scan   sensor_msgs/LaserScan
               /joint_states                    sensor_msgs/JointState
  publishes  : /vertical_gimbal/yaw_joint/cmd_pos    std_msgs/Float64  (rad)
               /vertical_gimbal/pitch_joint/cmd_pos  std_msgs/Float64  (rad)
               /vertical_gimbal/roll_joint/cmd_pos   std_msgs/Float64  (rad)
               /gimbal/mode                         std_msgs/String    (normal|focus)
"""

from __future__ import annotations

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy

from sensor_msgs.msg import JointState, LaserScan
from std_msgs.msg import Float64, String


class GimbalController(Node):

    def __init__(self) -> None:
        super().__init__('gimbal_controller')

        # ---- parameters -------------------------------------------------
        self.declare_parameter('normal_sweep_deg', 45.0)
        self.declare_parameter('focus_sweep_deg', 15.0)
        self.declare_parameter('normal_sweep_speed', 0.5)    # rad/s
        self.declare_parameter('focus_sweep_speed', 2.0)     # rad/s
        self.declare_parameter('obstacle_threshold', 3.0)    # m
        self.declare_parameter('focus_window_deg', 15.0)     # +/- around forward dir
        self.declare_parameter('focus_timeout', 2.0)         # s
        self.declare_parameter('control_rate', 50.0)         # Hz
        self.declare_parameter('joint_yaw_name', 'vertical_gimbal/yaw_joint')
        self.declare_parameter('joint_pitch_name', 'vertical_gimbal/pitch_joint')
        self.declare_parameter('joint_roll_name', 'vertical_gimbal/roll_joint')

        def p(n):
            return float(self.get_parameter(n).value)
        self.normal_half = math.radians(p('normal_sweep_deg'))
        self.focus_half = math.radians(p('focus_sweep_deg'))
        self.normal_speed = p('normal_sweep_speed')
        self.focus_speed = p('focus_sweep_speed')
        self.obstacle_threshold = p('obstacle_threshold')
        self.focus_window = math.radians(p('focus_window_deg'))
        self.focus_timeout = p('focus_timeout')
        self.joint_yaw_name = str(self.get_parameter('joint_yaw_name').value)
        self.joint_pitch_name = str(self.get_parameter('joint_pitch_name').value)
        self.joint_roll_name = str(self.get_parameter('joint_roll_name').value)

        # ---- state ------------------------------------------------------
        self.mode = 'normal'            # normal | focus
        self.position_yaw = 0.0         # current yaw command (rad)
        self.position_pitch = 0.0       # current pitch command (rad)
        self.position_roll = 0.0        # current roll command (rad)
        self.direction = 1              # triangle-wave direction
        self.joint_pos_yaw = 0.0        # measured joint angles
        self.joint_pos_pitch = 0.0
        self.joint_pos_roll = 0.0
        self.last_detection = None      # t of last in-window obstacle
        self.received_scan = False

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.create_subscription(LaserScan, '/vertical_gimbal_lidar/scan', self._on_scan, qos)
        self.create_subscription(JointState, '/joint_states', self._on_joint, 10)

        self.cmd_yaw_pub = self.create_publisher(Float64, self.joint_yaw_name, 10)
        self.cmd_pitch_pub = self.create_publisher(Float64, self.joint_pitch_name, 10)
        self.cmd_roll_pub = self.create_publisher(Float64, self.joint_roll_name, 10)
        self.mode_pub = self.create_publisher(String, '/gimbal/mode', 10)

        rate = p('control_rate')
        self.create_timer(1.0 / rate, self._on_timer)
        self.get_logger().info(
            '3D Gimbal controller up: sweep +/-%.0f deg @ %.2f rad/s, '
            'focus +/-%.0f deg @ %.2f rad/s'
            % (
                math.degrees(self.normal_half), self.normal_speed,
                math.degrees(self.focus_half), self.focus_speed,
            )
        )

    # ------------------------------------------------------------------ #
    def _on_joint(self, msg: JointState) -> None:
        """Track the measured gimbal joint positions so mode switches start from truth."""
        for name, pos in zip(msg.name, msg.position):
            if name == self.joint_yaw_name:
                self.joint_pos_yaw = pos
            elif name == self.joint_pitch_name:
                self.joint_pos_pitch = pos
            elif name == self.joint_roll_name:
                self.joint_pos_roll = pos

    def _on_scan(self, msg: LaserScan) -> None:
        """Detect obstacles inside the +/-15 deg forward horizontal window."""
        now = self.get_clock().now().nanoseconds * 1e-9
        self.received_scan = True

        best_range = math.inf

        for i, r in enumerate(msg.ranges):
            if not math.isfinite(r) or r < msg.range_min or r > msg.range_max:
                continue
            # Beam bearing in the drone body frame.
            # LiDAR angle=0 points forward along body X-axis.
            body_bearing = msg.angle_min + i * msg.angle_increment
            # Wrap to [-pi, pi]
            body_bearing = math.atan2(math.sin(body_bearing), math.cos(body_bearing))
            # Check if beam is within +/-focus_window of forward (body X-axis)
            if abs(body_bearing) <= self.focus_window and r < self.obstacle_threshold:
                best_range = min(best_range, r)

        if best_range < math.inf:
            self.last_detection = now
            if self.mode != 'focus':
                self.mode = 'focus'
                # Clamp the running commands inside the new (narrow) limits
                self.position_yaw = max(
                    -self.focus_half, min(self.focus_half, self.position_yaw)
                )
                self.position_pitch = max(
                    -self.focus_half, min(self.focus_half, self.position_pitch)
                )
                self.position_roll = 0.0  # keep level
                self.get_logger().info(
                    f'FOCUS mode: obstacle at {best_range:.2f} m in forward window'
                )
        elif (
            self.mode == 'focus'
            and self.last_detection is not None
            and now - self.last_detection > self.focus_timeout
        ):
            self.mode = 'normal'
            self.get_logger().info('NORMAL mode: focus timeout expired')

    # ------------------------------------------------------------------ #
    def _on_timer(self) -> None:
        """Advance the triangle wave inside the active limits and publish."""
        speed = self.focus_speed if self.mode == 'focus' else self.normal_speed
        half = self.focus_half if self.mode == 'focus' else self.normal_half

        dt = 1.0 / float(self.get_parameter('control_rate').value)
        self.position_yaw += self.direction * speed * dt

        # Bounce at the limit (triangle wave) for yaw
        if self.position_yaw >= half:
            self.position_yaw, self.direction = half, -1
        elif self.position_yaw <= -half:
            self.position_yaw, self.direction = -half, 1

        # Publish all three joint commands
        cmd_yaw = Float64(data=self.position_yaw)
        cmd_pitch = Float64(data=self.position_pitch)
        cmd_roll = Float64(data=self.position_roll)

        self.cmd_yaw_pub.publish(cmd_yaw)
        self.cmd_pitch_pub.publish(cmd_pitch)
        self.cmd_roll_pub.publish(cmd_roll)
        self.mode_pub.publish(String(data=self.mode))


def main(args=None) -> None:
    rclpy.init(args=args)
    node = GimbalController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
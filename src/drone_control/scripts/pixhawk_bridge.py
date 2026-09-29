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
Pixhawk4-style offboard bridge (MAVROS-compatible interface).

Bridges the MAVROS offboard velocity setpoint API to gz-sim's
MulticopterVelocityControl, without needing PX4 SITL:

  subscribes :
    /mavros/setpoint_velocity/cmd_vel_unstamped  geometry_msgs/Twist
        (ENU world-frame velocity setpoint, MAVROS convention)
    /mavros/state  isn't required; state is published below.
  publishes  :
    /mavros/state                 mavros_msgs/State   (connected/armed/guided)
    /mavros/local_position/odom   nav_msgs/Odometry   (ground truth mirror)
    /drone/cmd_vel                geometry_msgs/Twist (body-frame, to gz)
  services   :
    /mavros/set_mode              mavros_msgs/SetMode (returns OFFBOARD)
    /mavros/cmd/arming            mavros_msgs/CommandBool

The body-frame conversion uses ground-truth yaw, and a simple altitude
hold (P controller) supplies the vertical velocity channel.
"""

from __future__ import annotations

import math

from geometry_msgs.msg import Twist
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode
from nav_msgs.msg import Odometry
import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy


class PixhawkBridge(Node):

    def __init__(self) -> None:
        super().__init__('pixhawk_bridge')

        self.declare_parameter('cruise_altitude', 1.5)   # m (AGL hold)
        self.declare_parameter('publish_rate', 30.0)     # Hz

        self.cruise_alt = float(self.get_parameter('cruise_altitude').value)

        # ---- state ------------------------------------------------------
        self.connected = False
        self.armed = False
        self.mode = 'MANUAL'
        self.ekf_ok = True

        self.setpoint = Twist()          # last MAVROS setpoint (ENU)
        self.have_setpoint = False
        self.odom: Odometry | None = None

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        cb_group = ReentrantCallbackGroup()

        # ---- subscriptions ---------------------------------------------
        self.create_subscription(
            Twist,
            '/mavros/setpoint_velocity/cmd_vel_unstamped',
            self._on_setpoint,
            10,
            callback_group=cb_group,
        )
        self.create_subscription(
            Odometry, '/ground_truth/odometry', self._on_odom, qos,
            callback_group=cb_group,
        )

        # ---- publications ----------------------------------------------
        self.state_pub = self.create_publisher(State, '/mavros/state', 10)
        self.local_odom_pub = self.create_publisher(
            Odometry, '/mavros/local_position/odom', 10
        )
        self.cmd_pub = self.create_publisher(Twist, '/drone/cmd_vel', 10)

        # ---- services (MAVROS API surface) -----------------------------
        self.create_service(
            SetMode, '/mavros/set_mode', self._on_set_mode, callback_group=cb_group
        )
        self.create_service(
            CommandBool, '/mavros/cmd/arming', self._on_arm, callback_group=cb_group
        )

        rate = float(self.get_parameter('publish_rate').value)
        self.create_timer(1.0 / rate, self._on_control, callback_group=cb_group)
        self.create_timer(1.0, self._on_state, callback_group=cb_group)

        self.get_logger().info('Pixhawk bridge ready (MAVROS offboard interface)')

    # ------------------------------------------------------------------ #
    def _on_setpoint(self, msg: Twist) -> None:
        self.setpoint = msg
        self.have_setpoint = True

    def _on_odom(self, msg: Odometry) -> None:
        self.odom = msg
        if not self.connected:
            self.connected = True

    # ---- MAVROS services ---------------------------------------------- #
    def _on_set_mode(self, req, res: SetMode.Response) -> SetMode.Response:
        if req.custom_mode in ('OFFBOARD', 'GUIDED_NOGPS', ''):
            self.mode = req.custom_mode or 'OFFBOARD'
            res.mode_sent = True
            self.get_logger().info(f'Mode -> {self.mode}')
        else:
            # Accept anything: we are a soft FCU
            self.mode = req.custom_mode
            res.mode_sent = True
        return res

    def _on_arm(self, req, res: CommandBool.Response) -> CommandBool.Response:
        self.armed = bool(req.value)
        res.success = True
        res.result = 0
        self.get_logger().info(f'Armed -> {self.armed}')
        return res

    # ---- periodic outputs ---------------------------------------------- #
    def _on_state(self) -> None:
        s = State()
        stamp = self.get_clock().now().to_msg()
        s.stamp = stamp
        s.connected = self.connected
        s.armed = self.armed
        s.guided = self.mode in ('OFFBOARD', 'GUIDED', 'GUIDED_NOGPS')
        s.mode = self.mode
        self.state_pub.publish(s)

        if self.odom is not None:
            out = Odometry()
            out.header.stamp = stamp
            out.header.frame_id = 'odom'
            out.child_frame_id = 'base_link'
            out.pose = self.odom.pose
            out.twist = self.odom.twist
            self.local_odom_pub.publish(out)

    def _on_control(self) -> None:
        if self.odom is None:
            return

        cmd = Twist()

        # Only emit commands when armed (FCU-like gating)
        if self.armed:
            if self.mode in ('OFFBOARD', 'GUIDED', 'GUIDED_NOGPS') and self.have_setpoint:
                # MAVROS setpoints are ENU (world); convert to body frame
                yaw = self._yaw_from_odom()
                vx_w = self.setpoint.linear.x
                vy_w = self.setpoint.linear.y
                c, s = math.cos(yaw), math.sin(yaw)
                cmd.linear.x = c * vx_w + s * vy_w
                cmd.linear.y = -s * vx_w + c * vy_w
                cmd.angular.z = self.setpoint.angular.z
            # Altitude hold: P controller toward cruise altitude
            z = self.odom.pose.pose.position.z
            cmd.linear.z = max(-1.5, min(1.5, 0.8 * (self.cruise_alt - z)))

        self.cmd_pub.publish(cmd)

    def _yaw_from_odom(self) -> float:
        q = self.odom.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = PixhawkBridge()
    exec_ = MultiThreadedExecutor(num_threads=2)
    exec_.add_node(node)
    try:
        exec_.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

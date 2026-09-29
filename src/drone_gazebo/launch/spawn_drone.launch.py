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

"""Launch Gazebo house world, spawn the drone, start ros_gz bridges."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import xacro


def generate_launch_description() -> LaunchDescription:
    drone_gazebo_share = Path(get_package_share_directory('drone_gazebo'))
    drone_description_share = Path(get_package_share_directory('drone_description'))
    ros_gz_sim_share = Path(get_package_share_directory('ros_gz_sim'))

    use_sim_time = LaunchConfiguration('use_sim_time')
    world = LaunchConfiguration('world')

    # Process xacro -> robot_description string
    xacro_file = drone_description_share / 'urdf' / 'drone.xacro'
    robot_description = xacro.process_file(str(xacro_file)).toxml()

    bridge_config = str(drone_gazebo_share / 'config' / 'bridge.yaml')

    # gz sim -r <world>   (-s = server only, add via gz_args for headless)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(ros_gz_sim_share / 'launch' / 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': ['-v 3 -r ', world],
            'on_exit_shutdown': 'true',
        }.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description, 'use_sim_time': use_sim_time}
        ],
    )

    # Spawn once gz is up (delayed)
    spawn = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                output='screen',
                arguments=[
                    '-name', 'f450_drone',
                    '-topic', 'robot_description',
                    '-x', '0.0', '-y', '0.0', '-z', '0.15',
                ],
            )
        ],
    )

    # Config-file driven bridge: all sensor + command topics
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        parameters=[
            {'config_file': bridge_config},
            {'use_sim_time': use_sim_time},
        ],
    )

    # Optical flow approximation from ground truth
    optical_flow = Node(
        package='drone_gazebo',
        executable='optical_flow_approx.py',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument('use_sim_time', default_value='true'),
            DeclareLaunchArgument(
                'world',
                default_value=str(drone_gazebo_share / 'worlds' / 'sar_disaster.world'),
            ),
            gazebo,
            robot_state_publisher,
            spawn,
            bridge,
            optical_flow,
        ]
    )

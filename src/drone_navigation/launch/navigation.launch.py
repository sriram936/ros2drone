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
"""Launch the 3D motion primitives + navigation stack (frontier + RRT* + primitives)."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    use_sim_time = LaunchConfiguration('use_sim_time')

    params = str(
        Path(get_package_share_directory('drone_navigation'))
        / 'config'
        / 'nav_params.yaml'
    )

    def node(exec_name: str) -> Node:
        return Node(
            package='drone_navigation',
            executable=exec_name,
            name=exec_name.removesuffix('.py'),
            output='screen',
            parameters=[params, {'use_sim_time': use_sim_time}],
        )

    return LaunchDescription(
        [
            DeclareLaunchArgument('use_sim_time', default_value='true'),
            node('frontier_explorer.py'),
            node('rrt_star.py'),
            # 3D Motion Primitives for obstacle avoidance (enforced per spec)
            node('motion_primitives.py'),
            # DWA planner kept as fallback/secondary (optional)
            # node('dwa_planner.py'),
        ]
    )
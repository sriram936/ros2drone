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
Master simulation bringup.

Pipeline:
  gazebo house world + drone spawn + ros_gz bridges     (drone_gazebo)
  -> gimbal controller + pixhawk offboard bridge        (drone_control)
  -> 2.5D elevation mapper / SLAM                       (drone_slam)
  -> frontier exploration + RRT* + DWA                  (drone_navigation)
  -> RViz (optional, use_rviz:=true)

Usage:
  ros2 launch drone_bringup simulation.launch.py
  ros2 launch drone_bringup simulation.launch.py use_rviz:=true
  ros2 launch drone_bringup simulation.launch.py use_nav:=false
"""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def _include(pkg: str, rel_launch: str, condition=None, **launch_args):
    share = Path(get_package_share_directory(pkg))
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(share / rel_launch)),
        launch_arguments=launch_args.items() if launch_args else {}.items(),
        condition=condition,
    )


def generate_launch_description() -> LaunchDescription:
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_rviz = LaunchConfiguration('use_rviz')
    use_nav = LaunchConfiguration('use_nav')

    drone_bringup_share = Path(get_package_share_directory('drone_bringup'))

    # 1. World + spawn + bridges + optical flow
    gazebo = _include(
        'drone_gazebo', 'launch/spawn_drone.launch.py',
        use_sim_time=use_sim_time,
    )

    # 2. Gimbal controller + Pixhawk offboard bridge
    control = _include(
        'drone_control', 'launch/control.launch.py',
        use_sim_time=use_sim_time,
    )

    # 3. SLAM
    slam = _include(
        'drone_slam', 'launch/slam.launch.py',
        use_sim_time=use_sim_time,
    )

    # 4. Navigation stack (optional)
    nav = _include(
        'drone_navigation', 'launch/navigation.launch.py',
        condition=IfCondition(use_nav),
        use_sim_time=use_sim_time,
    )

    # 5. YOLOv26n NPU simulation (NPU split on Radxa Dragon Q6A)
    yolov26n = Node(
        package='drone_vision',
        executable='yolov26n_simulator.py',
        name='yolov26n_simulator',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    # 6. RViz (optional)
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d', str(drone_bringup_share / 'rviz' / 'drone.rviz'),
        ],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(use_rviz),
        output='screen',
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument('use_sim_time', default_value='true'),
            DeclareLaunchArgument('use_rviz', default_value='true'),
            DeclareLaunchArgument('use_nav', default_value='true'),
            gazebo,
            control,
            slam,
            nav,
            yolov26n,
            rviz,
        ]
    )

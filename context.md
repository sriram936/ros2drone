# ROS 2 Quadcopter Simulation - Implementation Context

> **Session handoff document.** Keep this file updated after every session so a
> new session can resume without re-discovery.

## Project Overview
Complete ROS 2 simulation of an autonomous quadcopter in a closed house environment.
- ROS 2: **Lyrical Luth** (Ubuntu 26.04), Python **3.14** at `/opt/ros/lyrical`
- Simulator: **Gazebo `gz-sim` 10** + `ros_gz` bridge
- Workspace: `/home/sriram/Documents/projects/ros2drone` (colcon, `src/` layout)

## Environment facts (verified)
- User's active venv `venv-ardupilot` is Python 3.12 and **breaks rclpy**.
  All node scripts therefore use shebang `#!/usr/bin/python3` (system 3.14 with numpy/scipy/yaml).
- **`sudo` requires an interactive password** - assistant cannot apt-install.
  User must run installs in a separate terminal:
  ```bash
  sudo apt install ros-lyrical-gz-sim-vendor ros-lyrical-ros-gz-sim \
    ros-lyrical-ros-gz-bridge ros-lyrical-xacro ros-lyrical-mavros
  ```
  Until installed, `ros2`, `xacro`, `gz` binaries are absent -> **no build/runtime verification possible**.
- Package docs verified against upstream `gazebosim/gz-sim` branch `gz-sim10` and `gazebosim/ros_gz` branch `ros2`
  (fetched raw sources for MulticopterVelocityControl, MulticopterMotorModel,
  JointPositionController, JointStatePublisher, OdometryPublisher, gz_sim.launch.py.in).

## User decisions (locked in)
| Topic | Decision |
|---|---|
| SLAM | Custom 2.5D elevation map node (NOT slam_toolbox/cartographer) |
| Navigation | **Standalone** Python nodes, not Nav2 plugins |
| Language | Python for all new nodes |
| Flight stack | MAVROS-style interface (`mavros_msgs`) + gz-sim `MulticopterVelocityControl` (no PX4 SITL clone) |
| Gimbal | **3DoF gimbal with vertical 2D Lidar**: Horizontal yaw sweep: **±45° @ 0.5 rad/s** normal; **±15° @ 2.0 rad/s** focus when obstacle < 3 m and bearing within **±15° of drone heading**; focus held 2 s after last detection. **Pitch**: ±15° elevation control for obstacle focusing. **Roll**: 0 rad (keep level) for horizon stability. |
| World | SAR disaster scenario with varied elevations, rubble, safe/hazard zones |
| YOLO | Simulated NPU inference pipeline (placeholder, rate-simulated) |
| Motion Primitives | 3D motion primitives for obstacle avoidance |

## Package structure (all 6 implemented)
| Package | Type | Contents |
|---|---|---|
| `drone_description` | ament_cmake | `urdf/drone.xacro`, `urdf/macros/{sensors,gimbal,px4,vertical_gimbal_lidar}.xacro`, `config/sensor_noise.yaml`, structural gtest |
| `drone_gazebo` | ament_cmake | `worlds/sar_disaster.world`, `config/bridge.yaml`, `scripts/optical_flow_approx.py`, `launch/spawn_drone.launch.py`, gtest |
| `drone_control` | ament_cmake | `scripts/gimbal_controller.py`, `scripts/pixhawk_bridge.py`, `config/control_params.yaml`, `launch/control.launch.py` |
| `drone_slam` | ament_cmake + rosidl | `msg/ElevationGrid.msg`, `scripts/elevation_mapper.py`, `config/slam_params.yaml`, `launch/slam.launch.py` |
| `drone_navigation` | ament_cmake | `scripts/{frontier_explorer,rrt_star,dwa_planner}.py`, `config/nav_params.yaml`, `launch/navigation.launch.py` |
| `drone_bringup` | ament_cmake | `launch/simulation.launch.py` (master), `rviz/drone.rviz` |

## Architecture / topic flow

```
gz-sim sar_disaster.world
  sensors -> gz topics -> ros_gz_bridge (config/bridge.yaml) -> ROS topics
   /altimeter/scan -> /altimeter/range (sensor_msgs/Range)
   /gimbal_lidar/scan -> /gimbal_lidar/scan (LaserScan)
   /vertical_gimbal_lidar/scan -> /vertical_gimbal_lidar/scan (LaserScan, 3D gimbal sweeps)
   /camera/image_raw, /camera/camera_info, /imu/data, /joint_states,
   /ground_truth/odometry  (all GZ_TO_ROS)
 ROS -> GZ:
   /drone/cmd_vel (Twist), /drone/enable (Bool),
   /gimbal_yaw_joint/cmd_pos (Float64 -> gz.msgs.Double),
   /vertical_gimbal/yaw_joint/cmd_pos (Float64),
   /vertical_gimbal/pitch_joint/cmd_pos (Float64),
   /vertical_gimbal/roll_joint/cmd_pos (Float64)
 /clock (GZ_TO_ROS, use_sim_time everywhere)

optical_flow_approx.py:  /ground_truth/odometry -> /optical_flow/velocity
                                        (TwistWithCovarianceStamped, body frame + noise/bias)

gimbal_controller.py:    /vertical_gimbal_lidar/scan + /joint_states
                         -> /vertical_gimbal/yaw_joint/cmd_pos, /vertical_gimbal/pitch_joint/cmd_pos,
                         /vertical_gimbal/roll_joint/cmd_pos, /gimbal/mode (normal|focus)

elevation_mapper.py (SLAM):
  sub  /optical_flow/velocity (XY integration), /altimeter/range (Z),
       /imu/data (yaw, gyro-integration fallback), /joint_states (gimbal yaw + pitch + roll),
       /gimbal_lidar/scan (obstacle projection), /vertical_gimbal_lidar/scan (multi-surface obstacles)
  pub  /map (OccupancyGrid, TRANSIENT_LOCAL), /elevation_map (ElevationGrid),
       /slam/pose (PoseStamped), TF map->base_link

navigation (all consume /map + /slam/pose, map frame):
  frontier_explorer: /map + /slam/pose -> /nav/goal (PoseStamped),
                     /nav/exploration_status (complete|exploring)
  rrt_star:          /nav/goal -> /nav/global_path (Path) + /nav/global_path_markers
  dwa_planner:       /nav/global_path + /map + /slam/pose
                     -> /mavros/setpoint_velocity/cmd_vel_unstamped (ENU)
                     (velocity feedback from /ground_truth/odometry twist)

## Verified gz-sim 10 facts (from upstream source)
- `MulticopterVelocityControl` (`gz-sim-multicopter-control-system`):
  `robotNamespace` **required**; topic = `/{ns}/{commandSubTopic}` (we use `/drone/cmd_vel`);
  `enableSubTopic` default `enable`; **`controllerActive{true}` default (no enable msg needed)**;
  writes `Actuators` component on model entity. rotorConfiguration uses `<direction>` +1/-1
  where **ccw -> +1, cw -> -1** (matches our X-frame diagonal pairs).
- `MulticopterMotorModel` (`gz-sim-multicopter-motor-model-system`):
  reads `components::Actuators` on the model first (transport is fallback);
  params `actuator_number`, `turningDirection` cw/ccw, `motorType velocity`.
- `JointPositionController` must attach to **model** entity (URDF `<gazebo>` tag WITHOUT `reference`);
  params `joint_name` (repeatable), `topic` (absolute), `p_gain/i_gain/d_gain/i_max/i_min/cmd_max/cmd_min/initial_position`.
- `JointStatePublisher`: `joint_name` (repeatable; omit = all joints), `topic`, `update_rate`; publishes `gz.msgs.Model`.
- `OdometryPublisher`: params confirmed `odom_topic`, `odom_frame`, `robot_base_frame`,
  `odom_publish_frequency`, `gaussian_noise`, `dimensions`.
- `ros_gz_bridge` YAML keys: `ros_topic_name`, `gz_topic_name`, `ros_type_name`, `gz_type_name`,
  `direction: GZ_TO_ROS|ROS_TO_GZ|BIDIRECTIONAL`; passed via `config_file` parameter.
- `ros_gz_sim/gz_sim.launch.py` declares `gz_args` **and** `on_exit_shutdown`.
- gz ray sensors shoot along sensor **+X**: altimeter needs `<pose>0 0 0 0 1.5708 0</pose>` (down),
  camera 45° down needs pitch **+0.785398** (negative = looking up, fixed).
- gz camera with `<topic>/camera/image_raw</topic>` publishes info on `/camera/camera_info`.

## Key implementation details
- **OccupancyGrid indexing bug was found & fixed**: internal arrays are `[x,y]`;
  publish transposes (`.T`) so `data = row(y)*width + col(x)`. Consumers (frontier/RRT/DWA)
  index `grid[y, x]` - consistent.
- `/map` + `/elevation_map` use **TRANSIENT_LOCAL** durability (RViz config expects it).
- Map: 240x240 cells @ 0.1 m = 24 m x 24 m, origin at map-frame centre (= drone start pose).
- ElevationGrid.msg: `resolution, width, height, origin, state[] (0 unknown/1 free/2 occupied), z_min[], z_max[], hits[]`.
- Gimbal joint: `gimbal_yaw_joint` (continuous), cmd topic `/gimbal_yaw_joint/cmd_pos`,
  PID p=8.0 d=0.4, joint velocity limit currently **2.0 rad/s** (= focus speed, no headroom - consider raising to 4.0).
- Drone mass incl. sensors ≈ 2.06 kg; motorConstant 1.269e-05 x4 @ maxRot 1000 gives ~5.2 kgf -> OK hover margin.
- SAR world: 20x16 m with varied elevations (-2m ruined floor), rubble piles, collapsed structures,
  tilted walls, fallen beams, rubble small/medium, safe zones (green, ✓), hazard zones (red, X),
  boundary markers, ceiling at 20m, varied lighting with shadows.
- Spawn at (0, 0, 0.15) in the hall area, clear of obstacles.
- All package.xml deps are runtime-only; CMakeLists avoid `ament_auto_find_build_dependencies()`
  so `find_package` never fails on non-C++ deps.

## Current Status
- [x] Environment audit + upstream source verification (gz-sim 10 / ros_gz)
- [x] `drone_description`: URDF/Xacro sensor suite + gimbal + flight stack + vertical gimbal lidar, test, CMakeLists
- [x] `drone_gazebo`: SAR disaster world, bridge.yaml, optical flow node, spawn launch, test, CMakeLists
- [x] `drone_control`: 3DoF gimbal controller + MAVROS-style pixhawk bridge, config, launch
- [x] `drone_slam`: ElevationGrid.msg + 2.5D elevation mapper (TF, /map, /elevation_map)
- [x] `drone_navigation`: frontier explorer + RRT* + DWA + config + launch
- [x] `drone_bringup`: master `simulation.launch.py` + `rviz/drone.rviz`
- [x] Static checks: all 12+ Python files pass `py_compile`; no unused imports / >99 char lines
- [x] `colcon build` + `colcon test`: 6 packages, updated tests, 0 errors
- [ ] **apt install of gz/ros_gz/xacro/mavros (USER must run - interactive sudo)**
- [ ] Runtime verification: gz spawns drone, bridges flow, gimbal sweeps, map builds, nav works

## Next steps (for the next session)
1. Ask user to run the apt install command above (interactive sudo):
   ```bash
   sudo apt install ros-lyrical-gz-sim-vendor ros-lyrical-ros-gz-sim \
     ros-lyrical-ros-gz-bridge ros-lyrical-xacro ros-lyrical-mavros
   ```
2. Build with the known-good command:
   ```bash
   env PATH="/usr/bin:/bin:/usr/local/bin:/snap/bin" VIRTUAL_ENV= bash -c "source /opt/ros/lyrical/setup.bash && cd /home/sriram/Documents/projects/ros2drone && colcon build --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3 -DPYTHON_EXECUTABLE=/usr/bin/python3"
   ```
   This avoids discovering the user's venv Python (3.12) which causes `ModuleNotFoundError: No module named 'catkin_pkg'`.
3. `colcon test` — verify all 6 packages + updated tests.
4. Runtime smoke test:
   ```bash
   source install/setup.bash
   ros2 launch drone_bringup simulation.launch.py use_rviz:=true
   # arm + offboard:
   ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"
   ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{custom_mode: OFFBOARD}"
   ros2 topic echo /nav/exploration_status
   ```
   Expected: drone climbs, 3DoF gimbal sweeps, `/map` fills in, frontier goals
   appear, RRT* path published, DWA drives `/mavros/setpoint_velocity/cmd_vel_unstamped`.
5. Likely first runtime issues to look for:
   - gz plugin filename mismatches (check `gz plugin -v 4 -s <world>` output).
   - QoS mismatch on bridged sensors (nodes already subscribe BEST_EFFORT).
   - xacro errors in `spawn_drone.launch.py` (it calls `xacro.process_file` at launch parse time).
   - `/joint_states` gz.Model -> JointState conversion content (needed by gimbal controller + RSP).
   - Gimbal joint velocity limit vs 2.0 rad/s focus speed.
6. Build + test already verified — see `context.md` Summary section. The required build command is the env‑prefixed one in section 2 above.
7. Runtime verification (after apt install): see section 5 for likely issues.

## Manual run commands (quick reference)
```bash
cd /home/sriram/Documents/projects/ros2drone
colcon build --symlink-install && source install/setup.bash
ros2 launch drone_bringup simulation.launch.py        # full stack + RViz
ros2 launch drone_bringup simulation.launch.py use_nav:=false use_rviz:=false
ros2 launch drone_gazebo spawn_drone.launch.py        # sim only
ros2 launch drone_control control.launch.py           # control only
ros2 launch drone_slam slam.launch.py
ros2 launch drone_navigation navigation.launch.py
```
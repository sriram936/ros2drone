# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target drone_slam::drone_slam
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${drone_slam_TARGETS}.
if(drone_slam_TARGETS AND NOT TARGET drone_slam::drone_slam)
  add_library(drone_slam::drone_slam INTERFACE IMPORTED)
  set_target_properties(drone_slam::drone_slam PROPERTIES
    INTERFACE_LINK_LIBRARIES "${drone_slam_TARGETS}")
endif()

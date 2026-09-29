// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

#ifndef DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include <cstddef>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "drone_slam/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "drone_slam/msg/detail/elevation_grid__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace drone_slam
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
cdr_serialize(
  const drone_slam::msg::ElevationGrid & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  drone_slam::msg::ElevationGrid & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
get_serialized_size(
  const drone_slam::msg::ElevationGrid & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
max_serialized_size_ElevationGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
cdr_serialize_key(
  const drone_slam::msg::ElevationGrid & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
get_serialized_size_key(
  const drone_slam::msg::ElevationGrid & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
max_serialized_size_key_ElevationGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
has_buffer_fields_ElevationGrid();

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace drone_slam

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_drone_slam
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, drone_slam, msg, ElevationGrid)();

#ifdef __cplusplus
}
#endif

#endif  // DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

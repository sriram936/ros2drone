// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice
#ifndef DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "drone_slam/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "drone_slam/msg/detail/elevation_grid__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
bool cdr_serialize_drone_slam__msg__ElevationGrid(
  const drone_slam__msg__ElevationGrid * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
bool cdr_deserialize_drone_slam__msg__ElevationGrid(
  eprosima::fastcdr::Cdr &,
  drone_slam__msg__ElevationGrid * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
size_t get_serialized_size_drone_slam__msg__ElevationGrid(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
size_t max_serialized_size_drone_slam__msg__ElevationGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
bool cdr_serialize_key_drone_slam__msg__ElevationGrid(
  const drone_slam__msg__ElevationGrid * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
size_t get_serialized_size_key_drone_slam__msg__ElevationGrid(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
size_t max_serialized_size_key_drone_slam__msg__ElevationGrid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
bool has_buffer_fields_drone_slam__msg__ElevationGrid();

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_drone_slam
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, drone_slam, msg, ElevationGrid)();

#ifdef __cplusplus
}
#endif

#endif  // DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_

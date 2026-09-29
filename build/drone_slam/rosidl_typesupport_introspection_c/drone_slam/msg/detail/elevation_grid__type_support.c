// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "drone_slam/msg/detail/elevation_grid__rosidl_typesupport_introspection_c.h"
#include "drone_slam/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "drone_slam/msg/detail/elevation_grid__functions.h"
#include "drone_slam/msg/detail/elevation_grid__struct.h"
#include "rosidl_buffer/c_helpers.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `origin`
#include "geometry_msgs/msg/pose.h"
// Member `origin`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `state`
// Member `z_min`
// Member `z_max`
// Member `hits`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  drone_slam__msg__ElevationGrid__init(message_memory);
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_fini_function(void * message_memory)
{
  drone_slam__msg__ElevationGrid__fini(message_memory);
}

size_t drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__state(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  if (member->is_rosidl_buffer) {
    rosidl_buffer_uint8_throw_if_not_cpu((const void *)member->data);
  }
  return member->size;
}

const void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__state(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  if (member->is_rosidl_buffer) {
    rosidl_buffer_uint8_throw_if_not_cpu((const void *)member->data);
  }
  return &member->data[index];
}

void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__state(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  if (member->is_rosidl_buffer) {
    rosidl_buffer_uint8_throw_if_not_cpu((const void *)member->data);
  }
  return &member->data[index];
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__state(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__state(untyped_member, index));
  uint8_t * value = (uint8_t *)(untyped_value);
  *value = *item;
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__state(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__state(untyped_member, index));
  const uint8_t * value = (const uint8_t *)(untyped_value);
  *item = *value;
}

bool drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__state(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  if (member->is_rosidl_buffer) {
    rosidl_buffer_uint8_throw_if_not_cpu((const void *)member->data);
  }
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

size_t drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__z_min(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__z_min(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__z_min(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__z_min(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__z_min(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__z_min(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__z_min(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__z_min(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__z_max(
  const void * untyped_member)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__z_max(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__float__Sequence * member =
    (const rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__z_max(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__z_max(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__z_max(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__z_max(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__z_max(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

bool drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__z_max(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__float__Sequence * member =
    (rosidl_runtime_c__float__Sequence *)(untyped_member);
  rosidl_runtime_c__float__Sequence__fini(member);
  return rosidl_runtime_c__float__Sequence__init(member, size);
}

size_t drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__hits(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint32__Sequence * member =
    (const rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  return member->size;
}

const void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__hits(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint32__Sequence * member =
    (const rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  return &member->data[index];
}

void * drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__hits(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint32__Sequence * member =
    (rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  return &member->data[index];
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__hits(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint32_t * item =
    ((const uint32_t *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__hits(untyped_member, index));
  uint32_t * value =
    (uint32_t *)(untyped_value);
  *value = *item;
}

void drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__hits(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint32_t * item =
    ((uint32_t *)
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__hits(untyped_member, index));
  const uint32_t * value =
    (const uint32_t *)(untyped_value);
  *item = *value;
}

bool drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__hits(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint32__Sequence * member =
    (rosidl_runtime_c__uint32__Sequence *)(untyped_member);
  rosidl_runtime_c__uint32__Sequence__fini(member);
  return rosidl_runtime_c__uint32__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_member_array[9] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "resolution",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, resolution),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "width",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "origin",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, origin),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, state),  // bytes offset in struct
    NULL,  // default value
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__state,  // size() function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__state,  // get_const(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__state,  // get(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__state,  // fetch(index, &value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__state,  // assign(index, value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__state,  // resize(index) function pointer
    true  // is_rosidl_buffer
  },
  {
    "z_min",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, z_min),  // bytes offset in struct
    NULL,  // default value
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__z_min,  // size() function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__z_min,  // get_const(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__z_min,  // get(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__z_min,  // fetch(index, &value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__z_min,  // assign(index, value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__z_min,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "z_max",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, z_max),  // bytes offset in struct
    NULL,  // default value
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__z_max,  // size() function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__z_max,  // get_const(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__z_max,  // get(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__z_max,  // fetch(index, &value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__z_max,  // assign(index, value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__z_max,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "hits",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam__msg__ElevationGrid, hits),  // bytes offset in struct
    NULL,  // default value
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__size_function__ElevationGrid__hits,  // size() function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_const_function__ElevationGrid__hits,  // get_const(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__get_function__ElevationGrid__hits,  // get(index) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__fetch_function__ElevationGrid__hits,  // fetch(index, &value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__assign_function__ElevationGrid__hits,  // assign(index, value) function pointer
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__resize_function__ElevationGrid__hits,  // resize(index) function pointer
    false  // is_rosidl_buffer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_members = {
  "drone_slam__msg",  // message namespace
  "ElevationGrid",  // message name
  9,  // number of fields
  sizeof(drone_slam__msg__ElevationGrid),
  false,  // has_any_key_member_
  drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_member_array,  // message members
  drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_init_function,  // function to initialize message memory (memory has to be allocated)
  drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_type_support_handle = {
  0,
  &drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_members,
  get_message_typesupport_handle_function,
  &drone_slam__msg__ElevationGrid__get_type_hash,
  &drone_slam__msg__ElevationGrid__get_type_description,
  &drone_slam__msg__ElevationGrid__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_drone_slam
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, drone_slam, msg, ElevationGrid)() {
  drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  if (!drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_type_support_handle.typesupport_identifier) {
    drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &drone_slam__msg__ElevationGrid__rosidl_typesupport_introspection_c__ElevationGrid_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

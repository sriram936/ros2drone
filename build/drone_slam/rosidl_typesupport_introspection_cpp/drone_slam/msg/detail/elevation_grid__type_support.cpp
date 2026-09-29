// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "drone_slam/msg/detail/elevation_grid__functions.h"
#include "drone_slam/msg/detail/elevation_grid__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"
#include "rosidl_buffer/buffer.hpp"

namespace drone_slam
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ElevationGrid_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) drone_slam::msg::ElevationGrid(_init);
}

void ElevationGrid_fini_function(void * message_memory)
{
  auto typed_message = static_cast<drone_slam::msg::ElevationGrid *>(message_memory);
  typed_message->~ElevationGrid();
}

size_t size_function__ElevationGrid__state(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const rosidl::Buffer<uint8_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ElevationGrid__state(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const rosidl::Buffer<uint8_t> *>(untyped_member);
  member.throw_if_not_cpu_backend();
  return &member[index];
}

void * get_function__ElevationGrid__state(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<rosidl::Buffer<uint8_t> *>(untyped_member);
  member.throw_if_not_cpu_backend();
  return &member[index];
}

void fetch_function__ElevationGrid__state(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint8_t *>(
    get_const_function__ElevationGrid__state(untyped_member, index));
  auto & value = *reinterpret_cast<uint8_t *>(untyped_value);
  value = item;
}

void assign_function__ElevationGrid__state(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint8_t *>(
    get_function__ElevationGrid__state(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint8_t *>(untyped_value);
  item = value;
}

void resize_function__ElevationGrid__state(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<rosidl::Buffer<uint8_t> *>(untyped_member);
  member->throw_if_not_cpu_backend();
  member->resize(size);
}

size_t size_function__ElevationGrid__z_min(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ElevationGrid__z_min(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__ElevationGrid__z_min(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__ElevationGrid__z_min(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__ElevationGrid__z_min(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__ElevationGrid__z_min(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__ElevationGrid__z_min(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__ElevationGrid__z_min(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ElevationGrid__z_max(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<float> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ElevationGrid__z_max(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<float> *>(untyped_member);
  return &member[index];
}

void * get_function__ElevationGrid__z_max(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<float> *>(untyped_member);
  return &member[index];
}

void fetch_function__ElevationGrid__z_max(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const float *>(
    get_const_function__ElevationGrid__z_max(untyped_member, index));
  auto & value = *reinterpret_cast<float *>(untyped_value);
  value = item;
}

void assign_function__ElevationGrid__z_max(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<float *>(
    get_function__ElevationGrid__z_max(untyped_member, index));
  const auto & value = *reinterpret_cast<const float *>(untyped_value);
  item = value;
}

void resize_function__ElevationGrid__z_max(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<float> *>(untyped_member);
  member->resize(size);
}

size_t size_function__ElevationGrid__hits(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<uint32_t> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ElevationGrid__hits(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<uint32_t> *>(untyped_member);
  return &member[index];
}

void * get_function__ElevationGrid__hits(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<uint32_t> *>(untyped_member);
  return &member[index];
}

void fetch_function__ElevationGrid__hits(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const uint32_t *>(
    get_const_function__ElevationGrid__hits(untyped_member, index));
  auto & value = *reinterpret_cast<uint32_t *>(untyped_value);
  value = item;
}

void assign_function__ElevationGrid__hits(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<uint32_t *>(
    get_function__ElevationGrid__hits(untyped_member, index));
  const auto & value = *reinterpret_cast<const uint32_t *>(untyped_value);
  item = value;
}

void resize_function__ElevationGrid__hits(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<uint32_t> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ElevationGrid_message_member_array[9] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "resolution",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, resolution),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "width",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, width),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "height",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, height),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "origin",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Pose>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, origin),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "state",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, state),  // bytes offset in struct
    nullptr,  // default value
    size_function__ElevationGrid__state,  // size() function pointer
    get_const_function__ElevationGrid__state,  // get_const(index) function pointer
    get_function__ElevationGrid__state,  // get(index) function pointer
    fetch_function__ElevationGrid__state,  // fetch(index, &value) function pointer
    assign_function__ElevationGrid__state,  // assign(index, value) function pointer
    resize_function__ElevationGrid__state,  // resize(index) function pointer
    true  // is_rosidl_buffer
  },
  {
    "z_min",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, z_min),  // bytes offset in struct
    nullptr,  // default value
    size_function__ElevationGrid__z_min,  // size() function pointer
    get_const_function__ElevationGrid__z_min,  // get_const(index) function pointer
    get_function__ElevationGrid__z_min,  // get(index) function pointer
    fetch_function__ElevationGrid__z_min,  // fetch(index, &value) function pointer
    assign_function__ElevationGrid__z_min,  // assign(index, value) function pointer
    resize_function__ElevationGrid__z_min,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "z_max",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, z_max),  // bytes offset in struct
    nullptr,  // default value
    size_function__ElevationGrid__z_max,  // size() function pointer
    get_const_function__ElevationGrid__z_max,  // get_const(index) function pointer
    get_function__ElevationGrid__z_max,  // get(index) function pointer
    fetch_function__ElevationGrid__z_max,  // fetch(index, &value) function pointer
    assign_function__ElevationGrid__z_max,  // assign(index, value) function pointer
    resize_function__ElevationGrid__z_max,  // resize(index) function pointer
    false  // is_rosidl_buffer
  },
  {
    "hits",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(drone_slam::msg::ElevationGrid, hits),  // bytes offset in struct
    nullptr,  // default value
    size_function__ElevationGrid__hits,  // size() function pointer
    get_const_function__ElevationGrid__hits,  // get_const(index) function pointer
    get_function__ElevationGrid__hits,  // get(index) function pointer
    fetch_function__ElevationGrid__hits,  // fetch(index, &value) function pointer
    assign_function__ElevationGrid__hits,  // assign(index, value) function pointer
    resize_function__ElevationGrid__hits,  // resize(index) function pointer
    false  // is_rosidl_buffer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ElevationGrid_message_members = {
  "drone_slam::msg",  // message namespace
  "ElevationGrid",  // message name
  9,  // number of fields
  sizeof(drone_slam::msg::ElevationGrid),
  false,  // has_any_key_member_
  ElevationGrid_message_member_array,  // message members
  ElevationGrid_init_function,  // function to initialize message memory (memory has to be allocated)
  ElevationGrid_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ElevationGrid_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ElevationGrid_message_members,
  get_message_typesupport_handle_function,
  &drone_slam__msg__ElevationGrid__get_type_hash,
  &drone_slam__msg__ElevationGrid__get_type_description,
  &drone_slam__msg__ElevationGrid__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace drone_slam


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<drone_slam::msg::ElevationGrid>()
{
  return &::drone_slam::msg::rosidl_typesupport_introspection_cpp::ElevationGrid_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, drone_slam, msg, ElevationGrid)() {
  return &::drone_slam::msg::rosidl_typesupport_introspection_cpp::ElevationGrid_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "drone_slam/msg/elevation_grid.hpp"


#ifndef DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__STRUCT_HPP_
#define DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_buffer/buffer.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'origin'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__drone_slam__msg__ElevationGrid __attribute__((deprecated))
#else
# define DEPRECATED__drone_slam__msg__ElevationGrid __declspec(deprecated)
#endif

namespace drone_slam
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ElevationGrid_
{
  using Type = ElevationGrid_<ContainerAllocator>;

  explicit ElevationGrid_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    origin(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->resolution = 0.0f;
      this->width = 0ul;
      this->height = 0ul;
    }
  }

  explicit ElevationGrid_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    origin(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->resolution = 0.0f;
      this->width = 0ul;
      this->height = 0ul;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _resolution_type =
    float;
  _resolution_type resolution;
  using _width_type =
    uint32_t;
  _width_type width;
  using _height_type =
    uint32_t;
  _height_type height;
  using _origin_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _origin_type origin;
  using _state_type =
    rosidl::Buffer<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _state_type state;
  using _z_min_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _z_min_type z_min;
  using _z_max_type =
    std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>>;
  _z_max_type z_max;
  using _hits_type =
    std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>>;
  _hits_type hits;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__resolution(
    const float & _arg)
  {
    this->resolution = _arg;
    return *this;
  }
  Type & set__width(
    const uint32_t & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__height(
    const uint32_t & _arg)
  {
    this->height = _arg;
    return *this;
  }
  Type & set__origin(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->origin = _arg;
    return *this;
  }
  Type & set__state(
    const rosidl::Buffer<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->state = _arg;
    return *this;
  }
  Type & set__z_min(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->z_min = _arg;
    return *this;
  }
  Type & set__z_max(
    const std::vector<float, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<float>> & _arg)
  {
    this->z_max = _arg;
    return *this;
  }
  Type & set__hits(
    const std::vector<uint32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint32_t>> & _arg)
  {
    this->hits = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    drone_slam::msg::ElevationGrid_<ContainerAllocator> *;
  using ConstRawPtr =
    const drone_slam::msg::ElevationGrid_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      drone_slam::msg::ElevationGrid_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      drone_slam::msg::ElevationGrid_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__drone_slam__msg__ElevationGrid
    std::shared_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__drone_slam__msg__ElevationGrid
    std::shared_ptr<drone_slam::msg::ElevationGrid_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ElevationGrid_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->resolution != other.resolution) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    if (this->origin != other.origin) {
      return false;
    }
    if (this->state != other.state) {
      return false;
    }
    if (this->z_min != other.z_min) {
      return false;
    }
    if (this->z_max != other.z_max) {
      return false;
    }
    if (this->hits != other.hits) {
      return false;
    }
    return true;
  }
  bool operator!=(const ElevationGrid_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ElevationGrid_

// alias to use template instance with default allocator
using ElevationGrid =
  drone_slam::msg::ElevationGrid_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace drone_slam

#endif  // DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__STRUCT_HPP_

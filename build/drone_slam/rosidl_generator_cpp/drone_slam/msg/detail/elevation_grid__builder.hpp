// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "drone_slam/msg/elevation_grid.hpp"


#ifndef DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__BUILDER_HPP_
#define DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "drone_slam/msg/detail/elevation_grid__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace drone_slam
{

namespace msg
{

namespace builder
{

class Init_ElevationGrid_hits
{
public:
  explicit Init_ElevationGrid_hits(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  ::drone_slam::msg::ElevationGrid hits(::drone_slam::msg::ElevationGrid::_hits_type arg)
  {
    msg_.hits = std::move(arg);
    return std::move(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_z_max
{
public:
  explicit Init_ElevationGrid_z_max(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  Init_ElevationGrid_hits z_max(::drone_slam::msg::ElevationGrid::_z_max_type arg)
  {
    msg_.z_max = std::move(arg);
    return Init_ElevationGrid_hits(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_z_min
{
public:
  explicit Init_ElevationGrid_z_min(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  Init_ElevationGrid_z_max z_min(::drone_slam::msg::ElevationGrid::_z_min_type arg)
  {
    msg_.z_min = std::move(arg);
    return Init_ElevationGrid_z_max(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_state
{
public:
  explicit Init_ElevationGrid_state(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  Init_ElevationGrid_z_min state(::drone_slam::msg::ElevationGrid::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_ElevationGrid_z_min(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_origin
{
public:
  explicit Init_ElevationGrid_origin(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  Init_ElevationGrid_state origin(::drone_slam::msg::ElevationGrid::_origin_type arg)
  {
    msg_.origin = std::move(arg);
    return Init_ElevationGrid_state(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_height
{
public:
  explicit Init_ElevationGrid_height(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  Init_ElevationGrid_origin height(::drone_slam::msg::ElevationGrid::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_ElevationGrid_origin(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_width
{
public:
  explicit Init_ElevationGrid_width(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  Init_ElevationGrid_height width(::drone_slam::msg::ElevationGrid::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_ElevationGrid_height(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_resolution
{
public:
  explicit Init_ElevationGrid_resolution(::drone_slam::msg::ElevationGrid & msg)
  : msg_(msg)
  {}
  Init_ElevationGrid_width resolution(::drone_slam::msg::ElevationGrid::_resolution_type arg)
  {
    msg_.resolution = std::move(arg);
    return Init_ElevationGrid_width(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

class Init_ElevationGrid_header
{
public:
  Init_ElevationGrid_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ElevationGrid_resolution header(::drone_slam::msg::ElevationGrid::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ElevationGrid_resolution(msg_);
  }

private:
  ::drone_slam::msg::ElevationGrid msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::drone_slam::msg::ElevationGrid>()
{
  return drone_slam::msg::builder::Init_ElevationGrid_header();
}

}  // namespace drone_slam

#endif  // DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__BUILDER_HPP_

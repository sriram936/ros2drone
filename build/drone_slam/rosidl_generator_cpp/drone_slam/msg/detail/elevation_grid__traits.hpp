// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "drone_slam/msg/elevation_grid.hpp"


#ifndef DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__TRAITS_HPP_
#define DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__TRAITS_HPP_

#include <stdint.h>

#include <array>
#include <cstddef>
#include <sstream>
#include <string>
#include <string_view>
#include <tuple>
#include <type_traits>
#include <utility>

#include "drone_slam/msg/detail/elevation_grid__struct.hpp"
#include "rosidl_runtime_cpp/buffer__traits.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'origin'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace drone_slam
{

namespace msg
{

inline void to_flow_style_yaml(
  const ElevationGrid & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: resolution
  {
    out << "resolution: ";
    rosidl_generator_traits::value_to_yaml(msg.resolution, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << ", ";
  }

  // member: origin
  {
    out << "origin: ";
    to_flow_style_yaml(msg.origin, out);
    out << ", ";
  }

  // member: state
  {
    if (msg.state.size() == 0) {
      out << "state: []";
    } else {
      out << "state: [";
      size_t pending_items = msg.state.size();
      for (auto item : msg.state) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: z_min
  {
    if (msg.z_min.size() == 0) {
      out << "z_min: []";
    } else {
      out << "z_min: [";
      size_t pending_items = msg.z_min.size();
      for (auto item : msg.z_min) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: z_max
  {
    if (msg.z_max.size() == 0) {
      out << "z_max: []";
    } else {
      out << "z_max: [";
      size_t pending_items = msg.z_max.size();
      for (auto item : msg.z_max) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: hits
  {
    if (msg.hits.size() == 0) {
      out << "hits: []";
    } else {
      out << "hits: [";
      size_t pending_items = msg.hits.size();
      for (auto item : msg.hits) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ElevationGrid & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: resolution
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "resolution: ";
    rosidl_generator_traits::value_to_yaml(msg.resolution, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }

  // member: origin
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "origin:\n";
    to_block_style_yaml(msg.origin, out, indentation + 2);
  }

  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.state.size() == 0) {
      out << "state: []\n";
    } else {
      out << "state:\n";
      for (auto item : msg.state) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: z_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.z_min.size() == 0) {
      out << "z_min: []\n";
    } else {
      out << "z_min:\n";
      for (auto item : msg.z_min) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: z_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.z_max.size() == 0) {
      out << "z_max: []\n";
    } else {
      out << "z_max:\n";
      for (auto item : msg.z_max) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: hits
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.hits.size() == 0) {
      out << "hits: []\n";
    } else {
      out << "hits:\n";
      for (auto item : msg.hits) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ElevationGrid & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

template<typename T, std::enable_if_t<std::is_same_v<std::decay_t<T>, drone_slam::msg::ElevationGrid>, int> = 0>
constexpr auto as_tuple_ref(T && msg)
{
  return std::forward_as_tuple(
    std::forward<T>(msg).header,
    std::forward<T>(msg).resolution,
    std::forward<T>(msg).width,
    std::forward<T>(msg).height,
    std::forward<T>(msg).origin,
    std::forward<T>(msg).state,
    std::forward<T>(msg).z_min,
    std::forward<T>(msg).z_max,
    std::forward<T>(msg).hits);
}

}  // namespace msg

}  // namespace drone_slam

namespace rosidl_generator_traits
{

template<>
constexpr const char * data_type<drone_slam::msg::ElevationGrid>()
{
  return "drone_slam::msg::ElevationGrid";
}

template<>
constexpr const char * name<drone_slam::msg::ElevationGrid>()
{
  return "drone_slam/msg/ElevationGrid";
}

template<>
struct has_fixed_size<drone_slam::msg::ElevationGrid>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<drone_slam::msg::ElevationGrid>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<drone_slam::msg::ElevationGrid>
  : std::true_type {};

template<>
struct MessageTraits<drone_slam::msg::ElevationGrid>
{
  static constexpr std::size_t member_count = 9;
  static constexpr std::array<std::string_view, member_count> member_names = {
    "header",
    "resolution",
    "width",
    "height",
    "origin",
    "state",
    "z_min",
    "z_max",
    "hits",
  };
};

}  // namespace rosidl_generator_traits

#endif  // DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__TRAITS_HPP_

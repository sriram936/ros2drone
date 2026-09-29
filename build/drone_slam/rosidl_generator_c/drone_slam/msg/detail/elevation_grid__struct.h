// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "drone_slam/msg/elevation_grid.h"


#ifndef DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__STRUCT_H_
#define DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'origin'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'state'
// Member 'z_min'
// Member 'z_max'
// Member 'hits'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/ElevationGrid in the package drone_slam.
/**
  * 2.5D multi-level (elevation) grid map.
  * One entry per cell, row-major (index = row * width + col).
 */
typedef struct drone_slam__msg__ElevationGrid
{
  std_msgs__msg__Header header;
  /// Metric size of one cell
  float resolution;
  /// Grid dimensions (cells)
  uint32_t width;
  uint32_t height;
  /// Pose of cell (0,0) center in the header frame
  geometry_msgs__msg__Pose origin;
  /// Cell classification (parallel arrays, row-major)
  /// 0 = unknown, 1 = free (observed, no obstacle), 2 = occupied
  rosidl_runtime_c__uint8__Sequence state;
  /// Lowest / highest observed obstacle return per cell (metres).
  /// NaN where no obstacle has been observed.
  rosidl_runtime_c__float__Sequence z_min;
  rosidl_runtime_c__float__Sequence z_max;
  /// Number of obstacle hits accumulated in the cell (confidence)
  rosidl_runtime_c__uint32__Sequence hits;
} drone_slam__msg__ElevationGrid;

// Struct for a sequence of drone_slam__msg__ElevationGrid.
typedef struct drone_slam__msg__ElevationGrid__Sequence
{
  drone_slam__msg__ElevationGrid * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} drone_slam__msg__ElevationGrid__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__STRUCT_H_

// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice
#include "drone_slam/msg/detail/elevation_grid__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `origin`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `state`
// Member `z_min`
// Member `z_max`
// Member `hits`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
drone_slam__msg__ElevationGrid__init(drone_slam__msg__ElevationGrid * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    drone_slam__msg__ElevationGrid__fini(msg);
    return false;
  }
  // resolution
  // width
  // height
  // origin
  if (!geometry_msgs__msg__Pose__init(&msg->origin)) {
    drone_slam__msg__ElevationGrid__fini(msg);
    return false;
  }
  // state
  if (!rosidl_runtime_c__uint8__Sequence__init(&msg->state, 0)) {
    drone_slam__msg__ElevationGrid__fini(msg);
    return false;
  }
  // z_min
  if (!rosidl_runtime_c__float__Sequence__init(&msg->z_min, 0)) {
    drone_slam__msg__ElevationGrid__fini(msg);
    return false;
  }
  // z_max
  if (!rosidl_runtime_c__float__Sequence__init(&msg->z_max, 0)) {
    drone_slam__msg__ElevationGrid__fini(msg);
    return false;
  }
  // hits
  if (!rosidl_runtime_c__uint32__Sequence__init(&msg->hits, 0)) {
    drone_slam__msg__ElevationGrid__fini(msg);
    return false;
  }
  return true;
}

void
drone_slam__msg__ElevationGrid__fini(drone_slam__msg__ElevationGrid * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // resolution
  // width
  // height
  // origin
  geometry_msgs__msg__Pose__fini(&msg->origin);
  // state
  rosidl_runtime_c__uint8__Sequence__fini(&msg->state);
  // z_min
  rosidl_runtime_c__float__Sequence__fini(&msg->z_min);
  // z_max
  rosidl_runtime_c__float__Sequence__fini(&msg->z_max);
  // hits
  rosidl_runtime_c__uint32__Sequence__fini(&msg->hits);
}

bool
drone_slam__msg__ElevationGrid__are_equal(const drone_slam__msg__ElevationGrid * lhs, const drone_slam__msg__ElevationGrid * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // resolution
  if (lhs->resolution != rhs->resolution) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  // origin
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->origin), &(rhs->origin)))
  {
    return false;
  }
  // state
  if (!rosidl_runtime_c__uint8__Sequence__are_equal(
      &(lhs->state), &(rhs->state)))
  {
    return false;
  }
  // z_min
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->z_min), &(rhs->z_min)))
  {
    return false;
  }
  // z_max
  if (!rosidl_runtime_c__float__Sequence__are_equal(
      &(lhs->z_max), &(rhs->z_max)))
  {
    return false;
  }
  // hits
  if (!rosidl_runtime_c__uint32__Sequence__are_equal(
      &(lhs->hits), &(rhs->hits)))
  {
    return false;
  }
  return true;
}

bool
drone_slam__msg__ElevationGrid__copy(
  const drone_slam__msg__ElevationGrid * input,
  drone_slam__msg__ElevationGrid * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // resolution
  output->resolution = input->resolution;
  // width
  output->width = input->width;
  // height
  output->height = input->height;
  // origin
  if (!geometry_msgs__msg__Pose__copy(
      &(input->origin), &(output->origin)))
  {
    return false;
  }
  // state
  if (!rosidl_runtime_c__uint8__Sequence__copy(
      &(input->state), &(output->state)))
  {
    return false;
  }
  // z_min
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->z_min), &(output->z_min)))
  {
    return false;
  }
  // z_max
  if (!rosidl_runtime_c__float__Sequence__copy(
      &(input->z_max), &(output->z_max)))
  {
    return false;
  }
  // hits
  if (!rosidl_runtime_c__uint32__Sequence__copy(
      &(input->hits), &(output->hits)))
  {
    return false;
  }
  return true;
}

drone_slam__msg__ElevationGrid *
drone_slam__msg__ElevationGrid__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_slam__msg__ElevationGrid * msg = (drone_slam__msg__ElevationGrid *)allocator.allocate(sizeof(drone_slam__msg__ElevationGrid), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(drone_slam__msg__ElevationGrid));
  bool success = drone_slam__msg__ElevationGrid__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
drone_slam__msg__ElevationGrid__destroy(drone_slam__msg__ElevationGrid * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    drone_slam__msg__ElevationGrid__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
drone_slam__msg__ElevationGrid__Sequence__init(drone_slam__msg__ElevationGrid__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_slam__msg__ElevationGrid * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(drone_slam__msg__ElevationGrid)) {
      return false;
    }
    data = (drone_slam__msg__ElevationGrid *)allocator.zero_allocate(size, sizeof(drone_slam__msg__ElevationGrid), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = drone_slam__msg__ElevationGrid__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        drone_slam__msg__ElevationGrid__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
drone_slam__msg__ElevationGrid__Sequence__fini(drone_slam__msg__ElevationGrid__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      drone_slam__msg__ElevationGrid__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

drone_slam__msg__ElevationGrid__Sequence *
drone_slam__msg__ElevationGrid__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  drone_slam__msg__ElevationGrid__Sequence * array = (drone_slam__msg__ElevationGrid__Sequence *)allocator.allocate(sizeof(drone_slam__msg__ElevationGrid__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = drone_slam__msg__ElevationGrid__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
drone_slam__msg__ElevationGrid__Sequence__destroy(drone_slam__msg__ElevationGrid__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    drone_slam__msg__ElevationGrid__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
drone_slam__msg__ElevationGrid__Sequence__are_equal(const drone_slam__msg__ElevationGrid__Sequence * lhs, const drone_slam__msg__ElevationGrid__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!drone_slam__msg__ElevationGrid__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
drone_slam__msg__ElevationGrid__Sequence__copy(
  const drone_slam__msg__ElevationGrid__Sequence * input,
  drone_slam__msg__ElevationGrid__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(drone_slam__msg__ElevationGrid)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(drone_slam__msg__ElevationGrid);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    drone_slam__msg__ElevationGrid * data =
      (drone_slam__msg__ElevationGrid *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!drone_slam__msg__ElevationGrid__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          drone_slam__msg__ElevationGrid__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!drone_slam__msg__ElevationGrid__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

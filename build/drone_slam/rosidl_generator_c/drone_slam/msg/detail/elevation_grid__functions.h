// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from drone_slam:msg/ElevationGrid.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "drone_slam/msg/elevation_grid.h"


#ifndef DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__FUNCTIONS_H_
#define DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "drone_slam/msg/rosidl_generator_c__visibility_control.h"

#include "drone_slam/msg/detail/elevation_grid__struct.h"

/// Initialize msg/ElevationGrid message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * drone_slam__msg__ElevationGrid
 * )) before or use
 * drone_slam__msg__ElevationGrid__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
bool
drone_slam__msg__ElevationGrid__init(drone_slam__msg__ElevationGrid * msg);

/// Finalize msg/ElevationGrid message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
void
drone_slam__msg__ElevationGrid__fini(drone_slam__msg__ElevationGrid * msg);

/// Create msg/ElevationGrid message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * drone_slam__msg__ElevationGrid__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
drone_slam__msg__ElevationGrid *
drone_slam__msg__ElevationGrid__create(void);

/// Destroy msg/ElevationGrid message.
/**
 * It calls
 * drone_slam__msg__ElevationGrid__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
void
drone_slam__msg__ElevationGrid__destroy(drone_slam__msg__ElevationGrid * msg);

/// Check for msg/ElevationGrid message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
bool
drone_slam__msg__ElevationGrid__are_equal(const drone_slam__msg__ElevationGrid * lhs, const drone_slam__msg__ElevationGrid * rhs);

/// Copy a msg/ElevationGrid message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
bool
drone_slam__msg__ElevationGrid__copy(
  const drone_slam__msg__ElevationGrid * input,
  drone_slam__msg__ElevationGrid * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
const rosidl_type_hash_t *
drone_slam__msg__ElevationGrid__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
const rosidl_runtime_c__type_description__TypeDescription *
drone_slam__msg__ElevationGrid__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
const rosidl_runtime_c__type_description__TypeSource *
drone_slam__msg__ElevationGrid__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
const rosidl_runtime_c__type_description__TypeSource__Sequence *
drone_slam__msg__ElevationGrid__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of msg/ElevationGrid messages.
/**
 * It allocates the memory for the number of elements and calls
 * drone_slam__msg__ElevationGrid__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
bool
drone_slam__msg__ElevationGrid__Sequence__init(drone_slam__msg__ElevationGrid__Sequence * array, size_t size);

/// Finalize array of msg/ElevationGrid messages.
/**
 * It calls
 * drone_slam__msg__ElevationGrid__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
void
drone_slam__msg__ElevationGrid__Sequence__fini(drone_slam__msg__ElevationGrid__Sequence * array);

/// Create array of msg/ElevationGrid messages.
/**
 * It allocates the memory for the array and calls
 * drone_slam__msg__ElevationGrid__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
drone_slam__msg__ElevationGrid__Sequence *
drone_slam__msg__ElevationGrid__Sequence__create(size_t size);

/// Destroy array of msg/ElevationGrid messages.
/**
 * It calls
 * drone_slam__msg__ElevationGrid__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
void
drone_slam__msg__ElevationGrid__Sequence__destroy(drone_slam__msg__ElevationGrid__Sequence * array);

/// Check for msg/ElevationGrid message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
bool
drone_slam__msg__ElevationGrid__Sequence__are_equal(const drone_slam__msg__ElevationGrid__Sequence * lhs, const drone_slam__msg__ElevationGrid__Sequence * rhs);

/// Copy an array of msg/ElevationGrid messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_drone_slam
bool
drone_slam__msg__ElevationGrid__Sequence__copy(
  const drone_slam__msg__ElevationGrid__Sequence * input,
  drone_slam__msg__ElevationGrid__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // DRONE_SLAM__MSG__DETAIL__ELEVATION_GRID__FUNCTIONS_H_

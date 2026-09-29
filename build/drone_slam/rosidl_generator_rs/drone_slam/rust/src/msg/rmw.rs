#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "drone_slam__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__drone_slam__msg__ElevationGrid() -> *const std::ffi::c_void;
}

#[link(name = "drone_slam__rosidl_generator_c")]
extern "C" {
    fn drone_slam__msg__ElevationGrid__init(msg: *mut ElevationGrid) -> bool;
    fn drone_slam__msg__ElevationGrid__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ElevationGrid>, size: usize) -> bool;
    fn drone_slam__msg__ElevationGrid__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ElevationGrid>);
    fn drone_slam__msg__ElevationGrid__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ElevationGrid>, out_seq: *mut rosidl_runtime_rs::Sequence<ElevationGrid>) -> bool;
}

// Corresponds to drone_slam__msg__ElevationGrid
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 2.5D multi-level (elevation) grid map.
/// One entry per cell, row-major (index = row * width + col).

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ElevationGrid {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// Metric size of one cell
    pub resolution: f32,

    /// Grid dimensions (cells)
    pub width: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub height: u32,

    /// Pose of cell (0,0) center in the header frame
    pub origin: geometry_msgs::msg::rmw::Pose,

    /// Cell classification (parallel arrays, row-major)
    /// 0 = unknown, 1 = free (observed, no obstacle), 2 = occupied
    pub state: rosidl_runtime_rs::Sequence<u8>,

    /// Lowest / highest observed obstacle return per cell (metres).
    /// NaN where no obstacle has been observed.
    pub z_min: rosidl_runtime_rs::Sequence<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z_max: rosidl_runtime_rs::Sequence<f32>,

    /// Number of obstacle hits accumulated in the cell (confidence)
    pub hits: rosidl_runtime_rs::Sequence<u32>,

}



impl Default for ElevationGrid {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !drone_slam__msg__ElevationGrid__init(&mut msg as *mut _) {
        panic!("Call to drone_slam__msg__ElevationGrid__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ElevationGrid {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_slam__msg__ElevationGrid__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_slam__msg__ElevationGrid__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { drone_slam__msg__ElevationGrid__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ElevationGrid {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ElevationGrid where Self: Sized {
  const TYPE_NAME: &'static str = "drone_slam/msg/ElevationGrid";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__drone_slam__msg__ElevationGrid() }
  }
}



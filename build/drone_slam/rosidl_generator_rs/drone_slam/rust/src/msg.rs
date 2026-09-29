#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to drone_slam__msg__ElevationGrid
/// 2.5D multi-level (elevation) grid map.
/// One entry per cell, row-major (index = row * width + col).

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ElevationGrid {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// Metric size of one cell
    pub resolution: f32,

    /// Grid dimensions (cells)
    pub width: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub height: u32,

    /// Pose of cell (0,0) center in the header frame
    pub origin: geometry_msgs::msg::Pose,

    /// Cell classification (parallel arrays, row-major)
    /// 0 = unknown, 1 = free (observed, no obstacle), 2 = occupied
    pub state: Vec<u8>,

    /// Lowest / highest observed obstacle return per cell (metres).
    /// NaN where no obstacle has been observed.
    pub z_min: Vec<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z_max: Vec<f32>,

    /// Number of obstacle hits accumulated in the cell (confidence)
    pub hits: Vec<u32>,

}



impl Default for ElevationGrid {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ElevationGrid::default())
  }
}

impl rosidl_runtime_rs::Message for ElevationGrid {
  type RmwMsg = super::msg::rmw::ElevationGrid;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        resolution: msg.resolution,
        width: msg.width,
        height: msg.height,
        origin: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.origin)).into_owned(),
        state: msg.state.as_slice().into(),
        z_min: msg.z_min.as_slice().into(),
        z_max: msg.z_max.as_slice().into(),
        hits: msg.hits.as_slice().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      resolution: msg.resolution,
      width: msg.width,
      height: msg.height,
        origin: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.origin)).into_owned(),
        state: msg.state.as_slice().into(),
        z_min: msg.z_min.as_slice().into(),
        z_max: msg.z_max.as_slice().into(),
        hits: msg.hits.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      resolution: msg.resolution,
      width: msg.width,
      height: msg.height,
      origin: geometry_msgs::msg::Pose::from_rmw_message(msg.origin),
      state: msg.state.into(),
      z_min: msg.z_min.into(),
      z_max: msg.z_max.into(),
      hits: msg.hits.into(),
    }
  }
}



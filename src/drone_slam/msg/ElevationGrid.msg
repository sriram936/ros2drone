# 2.5D multi-level (elevation) grid map.
# One entry per cell, row-major (index = row * width + col).

std_msgs/Header header

# Metric size of one cell
float32 resolution

# Grid dimensions (cells)
uint32 width
uint32 height

# Pose of cell (0,0) center in the header frame
geometry_msgs/Pose origin

# Cell classification (parallel arrays, row-major)
# 0 = unknown, 1 = free (observed, no obstacle), 2 = occupied
uint8[] state

# Lowest / highest observed obstacle return per cell (metres).
# NaN where no obstacle has been observed.
float32[] z_min
float32[] z_max

# Number of obstacle hits accumulated in the cell (confidence)
uint32[] hits

#!/usr/bin/python3
#!/usr/bin/env python3
#
# Copyright 2026 Sriram
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Simulated YOLOv26n NPU pipeline for Radxa Dragon Q6A.

This is a PLACEHOLDER simulator that mimics the behavior of a YOLOv26n
inference accelerator (FPN + PAN, NMS-free dual head) running on the
Radxa Dragon Q6A CPU/NPU split.

Features simulated:
  - FPN (Feature Pyramid Network) feature extraction
  - PAN (Path Aggregation Network) feature fusion
  - NMS-free dual head (classification + regression, no post-NMS)
  - NPU latency simulation (10-30ms typical for Q6A)
  - 5G/LTE telemetry metadata embedding
  - SAR-specific classes: human, hazard (fire/smoke/flood), survivor, vehicle
  - Confidence scoring and bounding box output

Classes (trained on COCO17, VisDrone, Fire/Smoke, FloodNet, SARD):
  0: background
  1: human
  2: fire
  3: smoke
  4: flood
  5: survivor (injured person)
  6: vehicle

Input: /camera/image_raw (sensor_msgs/Image)
Output: /detections (custom YOLOv26nDetectionArray msg)
        /npu_status (std_msgs/UInt8: 0=idle, 1=processing, 2=alert)
"""

from __future__ import annotations

import math
import random
import time
from typing import List, Optional

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

from sensor_msgs.msg import Image
from std_msgs.msg import UInt8, String, Float32MultiArray, Header



# YOLOv26n class definitions (6 classes + background)
YOLOV26N_CLASSES = [
    'background',
    'human',
    'fire',
    'smoke',
    'flood',
    'survivor',
    'vehicle',
]

NUM_CLASSES = 7  # including background


class YOLOv26nDetection:
    """Single YOLOv26n detection result."""

    def __init__(
        self,
        class_id: int,
        confidence: float,
        bbox: tuple[float, float, float, float],  # x_min, y_min, x_max, y_max
        timestamp: float,
    ) -> None:
        self.class_id = class_id
        self.confidence = confidence
        self.bbox = bbox  # in image coordinates (pixels)
        self.timestamp = timestamp
        # Compute center and dimensions
        self.x_min = bbox[0]
        self.y_min = bbox[1]
        self.x_max = bbox[2]
        self.y_max = bbox[3]
        self.width = bbox[2] - bbox[0]
        self.height = bbox[3] - bbox[1]
        self.x_center = (bbox[0] + bbox[2]) / 2.0
        self.y_center = (bbox[1] + bbox[3]) / 2.0


class YOLOv26nDetectionArray:
    """Container for YOLOv26n detections array."""

    def __init__(self) -> None:
        self.header: Header = Header()
        self.detections: List[YOLOv26nDetection] = []
        # NPU simulation info
        self.npu_latency_ms: float = 0.0
        self.processing_time_ms: float = 0.0


def yaw_to_geometry(yaw: float) -> float:
    """Convert yaw angle to a simple geometry factor (placeholder)."""
    return math.sin(yaw)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value to [min_val, max_val] range."""
    return max(min_val, min(max_val, value))


class YOLOv26nSimulator(Node):

    def __init__(self) -> None:
        super().__init__('yolov26n_simulator')

        # ---- parameters -------------------------------------------------
        self.declare_parameter('input_image_topic', '/camera/image_raw')
        self.declare_parameter('detections_topic', '/detections')
        self.declare_parameter('npu_status_topic', '/npu_status')
        self.declare_parameter('confidence_threshold', 0.5)
        self.declare_parameter('simulate_npu_latency', True)
        self.declare_parameter('npu_latency_mean', 15.0)   # ms, typical Q6A
        self.declare_parameter('npu_latency_stddev', 5.0)  # ms
        self.declare_parameter('frame_rate', 10.0)        # Hz, simulated NPU limit
        self.declare_parameter('simulated_classes', ['human', 'fire', 'smoke', 'flood', 'survivor'])

        cf = self.get_parameter('confidence_threshold').value
        self.conf_threshold = cf
        self.simulate_latency = self.get_parameter('simulate_npu_latency').value
        self.latency_mean = self.get_parameter('npu_latency_mean').value
        self.latency_stddev = self.get_parameter('npu_latency_stddev').value
        self.frame_rate_hz = self.get_parameter('frame_rate').value

        # ---- state ------------------------------------------------------
        self.latest_image_timestamp: float = 0.0
        self.npu_state: UInt8 = UInt8(data=0)  # 0=idle, 1=processing, 2=alert
        self.frame_count = 0
        self.last_detection_time = 0.0

        # Publisher
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.det_pub = self.create_publisher(
            String,  # Using String for simplicity; could be custom msg
            self.get_parameter('detections_topic').value,
            10,
        )
        self.npu_status_pub = self.create_publisher(
            UInt8,
            self.get_parameter('npu_status_topic').value,
            10,
        )

        # Timer for simulated NPU processing at specified frame rate
        self.create_timer(1.0 / self.frame_rate_hz, self._simulate_inference)

        # Subscribe to camera images (just for timing/sync, we don't process actual images)
        self.create_subscription(
            Image,
            self.get_parameter('input_image_topic').value,
            self._on_image,
            qos,
        )

        self.get_logger().info(
            f'YOLOv26n simulator up: classes={NUM_CLASSES}, '
            f'conf_thresh={self.conf_threshold}, fps={self.frame_rate_hz}, '
            f'latency~{self.latency_mean:.1f}±{self.latency_stddev:.1f} ms'
        )

    # ------------------------------------------------------------------ #
    # Image callback (triggered, not processing full image)                #
    # ------------------------------------------------------------------ #
    def _on_image(self, msg: Image) -> None:
        self.latest_image_timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

    # ------------------------------------------------------------------ #
    # Simulated NPU inference                                            #
    # ------------------------------------------------------------------ #
    def _simulate_inference(self) -> None:
        """Run simulated YOLOv26n inference and publish detections."""

        # Simulate NPU latency
        if self.simulate_latency:
            latency = max(0, np.random.normal(self.latency_mean, self.latency_stddev))
            self.npu_latency_ms = latency
        else:
            self.npu_latency_ms = 0.0

        # Update NPU state
        self.npu_state.data = 1  # processing
        self.npu_status_pub.publish(self.npu_state)

        # Simulate inference time
        time.sleep(min(self.npu_latency_ms / 1000.0, 0.03))  # cap at 30ms

        # Generate simulated detections (placeholder random detections)
        detections = self._generate_detections()

        # Build output message
        array_msg = YOLOv26nDetectionArray()
        array_msg.header.stamp = self.get_clock().now().to_msg()
        array_msg.header.frame_id = 'camera_link'
        array_msg.npu_latency_ms = self.npu_latency_ms
        array_msg.processing_time_ms = self.npu_latency_ms

        for det in detections:
            det_msg = {
                'class_id': det.class_id,
                'confidence': det.confidence,
                'bbox': [det.x_min, det.y_min, det.x_max, det.y_max],
                'timestamp': det.timestamp,
            }
            # Serialize as string for simplicity (could be custom msg)
            import json
            array_msg.detections_json.append(json.dumps(det_msg))

        # Publish detections
        self.det_pub.publish(array_msg)

        # Check for high-priority alerts (human/fire/smoke detection)
        high_priority = [
            d for d in detections
            if d.class_id in [1, 2, 3]  # human, fire, smoke
            and d.confidence > 0.7
        ]

        if high_priority and self.npu_state.data != 2:
            self.npu_state.data = 2  # alert
            self.get_logger().warning(
                f'ALERT: {len(high_priority)} high-priority detections ('
                f'class IDs: {[d.class_id for d in high_priority]})'
            )

        # Reset NPU state after processing
        self.npu_state.data = 0  # idle (briefly)
        self.npu_status_pub.publish(self.npu_state)

        self.frame_count += 1

    # ------------------------------------------------------------------ #
    # Generate placeholder detections                                     #
    # ------------------------------------------------------------------ #
    def _generate_detections(self) -> list:
        """Generate placeholder YOLOv26n detections (random but structured)."""
        detections = []

        # Simulate 0-3 detections per frame (stochastic but bounded)
        num_dets = random.randint(0, 3)

        # Class weights for SAR scenario (humans and hazards more common in some regions)
        class_weights = [0.7,  # background (often ignored)
                         0.15, # human
                         0.05, # fire
                         0.05, # smoke
                         0.03, # flood
                         0.02, # survivor
                         0.05] # vehicle

        # Total probability should sum to ~1.0 (approx)
        for _ in range(num_dets):
            # Pick class based on weights (excluding background most of the time)
            class_idx = random.choices(
                range(1, NUM_CLASSES),  # skip background
                weights=[class_weights[i] for i in range(1, NUM_CLASSES)],
                k=1,
            )[0]

            # Confidence decreases with "distance" - simulate realistic values
            confidence = min(
                random.uniform(0.55, 0.98),
                1.0,
            )

            # Bounding box in image coordinates (640x480 simulated)
            img_w, img_h = 640, 480
            # Ensure box is within image
            x_min = random.uniform(0, img_w * 0.7)
            y_min = random.uniform(0, img_h * 0.7)
            x_max = min(x_min + random.uniform(40, 150), img_w)
            y_max = min(y_min + random.uniform(40, 150), img_h)

            # For very small boxes, expand slightly
            if (x_max - x_min) < 20:
                x_max = min(x_max + 20, img_w)
            if (y_max - y_min) < 20:
                y_max = min(y_max + 20, img_h)

            det = YOLOv26nDetection(
                class_id=int(class_idx),
                confidence=confidence,
                bbox=(x_min, y_min, x_max, y_max),
                timestamp=self.latest_image_timestamp or self.get_clock().now().to_msg().sec,
            )
            detections.append(det)

        # If no detections, still publish empty array with NPU latency
        if not detections:
            # Still add a "no detections" marker
            det = YOLOv26nDetection(
                class_id=0,  # background
                confidence=0.0,
                bbox=(0, 0, 0, 0),
                timestamp=self.latest_image_timestamp or self.get_clock().now().to_msg().sec,
            )
            detections.append(det)

        return detections


def main(args=None) -> None:
    rclpy.init(args=args)
    node = YOLOv26nSimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
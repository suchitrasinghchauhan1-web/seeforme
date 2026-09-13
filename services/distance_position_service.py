import cv2
import torch
import numpy as np

from PIL import Image
from transformers import DPTImageProcessor, DPTForDepthEstimation


# ========================================
# SETTINGS
# ========================================

DEPTH_MODEL_NAME = "Intel/dpt-hybrid-midas"


# ========================================
# LOAD DEPTH MODEL
# ========================================

print("Loading Depth model...")

processor = DPTImageProcessor.from_pretrained(
    DEPTH_MODEL_NAME
)

depth_model = DPTForDepthEstimation.from_pretrained(
    DEPTH_MODEL_NAME
)

print("Depth model loaded successfully!")


# ========================================
# POSITION DETECTION
# ========================================

def get_position(center_x, width):

    left_boundary = width // 3
    right_boundary = (width * 2) // 3

    if center_x < left_boundary:
        return "left"

    elif center_x > right_boundary:
        return "right"

    else:
        return "center"


# ========================================
# DEPTH DETECTION
# ========================================

def detect_depth(frame):

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    image = Image.fromarray(rgb)

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = depth_model(**inputs)

    depth = outputs.predicted_depth

    depth = torch.nn.functional.interpolate(
        depth.unsqueeze(1),
        size=image.size[::-1],
        mode="bicubic",
        align_corners=False
    )

    depth = depth.squeeze().cpu().numpy()

    return depth


# ========================================
# DISTANCE ESTIMATION
# ========================================

def get_distance(
    depth_value,
    depth_min,
    depth_max
):

    difference = depth_max - depth_min

    if difference < 0.0001:

        return 2.0

    normalized = (
        (depth_value - depth_min)
        / difference
    )

    normalized = np.clip(
        normalized,
        0,
        1
    )

    distance = 5.0 - (
        normalized * 4.5
    )

    distance = max(
        0.5,
        min(5.0, distance)
    )

    return float(distance)


# ========================================
# ADD POSITION AND DISTANCE
# ========================================

def add_position_and_distance(
    frame,
    objects
):

    height, width, _ = frame.shape

    # Calculate depth map
    depth_map = detect_depth(frame)

    # Find useful depth range
    depth_min = np.percentile(
        depth_map,
        2
    )

    depth_max = np.percentile(
        depth_map,
        98
    )

    updated_objects = []

    for obj in objects:

        # Get bounding box
        x1, y1, x2, y2 = obj["bbox"]

        # Calculate center
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Keep coordinates inside image
        center_x = min(
            max(center_x, 0),
            width - 1
        )

        center_y = min(
            max(center_y, 0),
            height - 1
        )

        # Get position
        position = get_position(
            center_x,
            width
        )

        # Get depth value
        depth_value = depth_map[
            center_y,
            center_x
        ]

        # Convert depth to estimated distance
        distance = get_distance(
            depth_value,
            depth_min,
            depth_max
        )

        # Add information
        updated_objects.append({

            "name": obj["name"],

            "confidence": obj["confidence"],

            "distance": distance,

            "position": position

        })

    return updated_objects
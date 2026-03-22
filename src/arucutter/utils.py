import cv2
import numpy as np
from arucutter.aruco import ArucoMarker
import os

def deskew_and_crop(
    image_path: str,
    src_points: np.ndarray,
    dst_width: int,
    dst_height: int,
    output_path: str = "arucos/output/deskewed.png"
):
    """
    image_path : path to input image
    src_points : 4x2 array-like of (x, y) in source image
                 order: top-left, top-right, bottom-right, bottom-left
    dst_width  : width of output rectangle in pixels
    dst_height : height of output rectangle in pixels
    output_path: where to save result
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Ensure float32 and correct shape
    src = np.array(src_points, dtype=np.float32).reshape(4, 2)

    # Destination rectangle
    dst = np.array(
        [
            [0, 0],
            [dst_width - 1, 0],
            [dst_width - 1, dst_height - 1],
            [0, dst_height - 1],
        ],
        dtype=np.float32,
    )

    # Perspective transform matrix
    M = cv2.getPerspectiveTransform(src, dst)

    # Warp (deskew) to desired size
    warped = cv2.warpPerspective(img, M, (dst_width, dst_height))

    # Save and also return the result
    cv2.imwrite(output_path, warped)
    return warped

def rescale(frame, scales = (0.8, 0.3)):
    width = int(frame.shape[1] * scales[0])
    height = int(frame.shape[0] * scales[1])
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
        
def describe_image(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Could not load image: {path}")

    shape = img.shape

    # Height and width
    height = shape[0]
    width = shape[1]

    # Determine color mode based on number of channels
    if len(shape) == 2:
        color_mode = "grayscale"
        channels = 1
    elif len(shape) == 3:
        channels = shape[2]
        if channels == 3:
            color_mode = "BGR (color)"
        elif channels == 4:
            color_mode = "BGRA (color with alpha)"
        else:
            color_mode = f"{channels}-channel image"
    else:
        color_mode = "unknown"
        channels = None
    
    return {'width': width,
            'height': height,
            'channels': channels,
            'color_mode': color_mode}

"""
Image processing utilities.
"""

import base64
import io
from typing import Optional

import cv2
import numpy as np
from PIL import Image

def decode_base64_image(base64_str: str) -> Optional[np.ndarray]:
    """
    Decode a base64 encoded image string to an OpenCV format (BGR numpy array).
    """
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
            
        img_data = base64.b64decode(base64_str)
        img_np = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None

def encode_image_base64(img: np.ndarray, quality: int = 80) -> str:
    """
    Encode an OpenCV image to a base64 string.
    """
    _, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return base64.b64encode(buffer).decode('utf-8')

def resize_with_aspect_ratio(image: np.ndarray, width: Optional[int] = None, height: Optional[int] = None, inter: int = cv2.INTER_AREA) -> np.ndarray:
    """
    Resize an image while maintaining its aspect ratio.
    """
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

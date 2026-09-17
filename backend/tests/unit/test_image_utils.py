"""
Unit tests for image_utils.
"""

import base64
import numpy as np

import cv2
from app.utils.image_utils import decode_base64_image, encode_image_base64, resize_with_aspect_ratio


def test_encode_decode_base64():
    # Create a simple 10x10 black image
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    
    # Encode
    encoded = encode_image_base64(img)
    assert isinstance(encoded, str)
    assert len(encoded) > 0
    
    # Decode
    decoded = decode_base64_image(encoded)
    assert decoded is not None
    assert decoded.shape == (10, 10, 3)


def test_resize_with_aspect_ratio():
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    
    # Resize width to 50, height should become 25
    resized = resize_with_aspect_ratio(img, width=50)
    assert resized.shape[:2] == (25, 50)
    
    # Resize height to 200, width should become 400
    resized = resize_with_aspect_ratio(img, height=200)
    assert resized.shape[:2] == (200, 400)

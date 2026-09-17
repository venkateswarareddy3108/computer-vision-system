"""
Geometric calculations (e.g., Euclidean distance, point manipulation).
"""

import math
from typing import Tuple

import numpy as np


def euclidean_distance(pt1: Tuple[float, float], pt2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two 2D points.
    """
    return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


def get_center_point(bbox: Tuple[float, float, float, float]) -> Tuple[float, float]:
    """
    Calculate the center point of a bounding box.
    """
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    """
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    return dot_product / (norm_a * norm_b)

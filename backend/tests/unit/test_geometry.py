"""
Unit tests for geometry utils.
"""

import numpy as np
import pytest

from app.utils.geometry import cosine_similarity, euclidean_distance, get_center_point


def test_euclidean_distance():
    pt1 = (0.0, 0.0)
    pt2 = (3.0, 4.0)
    assert euclidean_distance(pt1, pt2) == 5.0


def test_get_center_point():
    bbox = (10, 10, 30, 50)
    assert get_center_point(bbox) == (20.0, 30.0)


def test_cosine_similarity():
    vec1 = np.array([1.0, 0.0])
    vec2 = np.array([0.0, 1.0])
    assert cosine_similarity(vec1, vec2) == 0.0

    vec3 = np.array([1.0, 0.0])
    vec4 = np.array([1.0, 0.0])
    assert pytest.approx(cosine_similarity(vec3, vec4)) == 1.0

"""
Unit tests for finger_counter.
"""

import numpy as np

from app.vision.finger_counter import FingerCounter


def test_finger_counter_initialization():
    counter = FingerCounter()
    assert counter is not None


def test_finger_counting_empty_landmarks():
    counter = FingerCounter()
    # Should handle empty gracefully or return 0
    count = counter.count(None, "Right")
    assert count == 0

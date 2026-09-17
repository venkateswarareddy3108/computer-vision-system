"""
Unit tests for eye_analyzer.
"""

import numpy as np
import pytest

from app.vision.eye_analyzer import EARAnalyzer


def test_ear_analyzer_initialization():
    analyzer = EARAnalyzer(history_size=30)
    assert analyzer.history_size == 30
    assert len(analyzer.ear_history) == 0


def test_ear_analyzer_empty():
    analyzer = EARAnalyzer()
    result = analyzer.analyze(None)
    assert result["eye_state"] == "unknown"
    assert result["awake_status"] == "unknown"

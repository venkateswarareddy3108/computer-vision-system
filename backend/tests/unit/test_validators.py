"""
Unit tests for validators.
"""

from unittest.mock import MagicMock

import pytest

from app.core.exceptions import ValidationException
from app.utils.validators import validate_image_file


def test_validate_image_file_valid():
    mock_file = MagicMock()
    mock_file.filename = "test.jpg"
    mock_file.content_type = "image/jpeg"
    
    # Should not raise exception
    validate_image_file(mock_file)


def test_validate_image_file_invalid_ext():
    mock_file = MagicMock()
    mock_file.filename = "test.pdf"
    mock_file.content_type = "application/pdf"
    
    with pytest.raises(ValidationException):
        validate_image_file(mock_file)


def test_validate_image_file_invalid_content_type():
    mock_file = MagicMock()
    mock_file.filename = "test.jpg"
    mock_file.content_type = "text/plain"
    
    with pytest.raises(ValidationException):
        validate_image_file(mock_file)

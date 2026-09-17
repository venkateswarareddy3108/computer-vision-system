"""
Validation utilities for files, input shapes, etc.
"""

from fastapi import UploadFile

from app.core.exceptions import ValidationException

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_FILE_SIZE_MB = 10


def validate_image_file(file: UploadFile) -> None:
    """
    Validate that an uploaded file is a supported image and within size limits.
    """
    # Check extension
    filename = file.filename
    if not filename:
        raise ValidationException("No filename provided")
        
    ext = filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationException(f"Unsupported file extension: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
        
    # Check content type
    if not file.content_type.startswith("image/"):
        raise ValidationException("File is not an image")
        
    # Size check is usually better done via middleware or read chunks
    # This is a basic stub
    pass

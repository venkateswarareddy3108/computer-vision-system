"""
Security utilities: CORS configuration, file upload validation,
secure filename handling, and path traversal protection.
"""

from __future__ import annotations

import os
import re
import uuid
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def configure_cors(app: FastAPI) -> None:
    """Configure CORS middleware with allowed origins from settings."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def sanitize_filename(filename: str) -> str:
    """
    Generate a secure filename to prevent path traversal attacks.

    Strips directory components, removes unsafe characters,
    and prepends a UUID to ensure uniqueness.
    """
    # Extract just the filename (no directory path)
    basename = os.path.basename(filename)

    # Remove any non-alphanumeric characters except dots, hyphens, underscores
    safe_name = re.sub(r"[^\w\-.]", "_", basename)

    # Prepend UUID for uniqueness
    unique_prefix = uuid.uuid4().hex[:12]
    return f"{unique_prefix}_{safe_name}"


def validate_file_extension(filename: str, allowed_extensions: List[str] | None = None) -> bool:
    """Check if the file extension is in the allowed list."""
    if allowed_extensions is None:
        allowed_extensions = settings.allowed_extensions_list

    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in allowed_extensions


def validate_upload_path(upload_dir: str, filepath: str) -> bool:
    """
    Validate that the resolved file path is within the upload directory.

    Prevents path traversal attacks like ../../etc/passwd.
    """
    upload_dir_resolved = Path(upload_dir).resolve()
    filepath_resolved = Path(filepath).resolve()
    return str(filepath_resolved).startswith(str(upload_dir_resolved))


def get_upload_dir() -> Path:
    """Get the upload directory path, creating it if necessary."""
    upload_dir = Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

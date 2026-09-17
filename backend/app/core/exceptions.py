"""
Custom exception hierarchy and centralized FastAPI exception handlers.

All exceptions return sanitized error messages in production.
Stack traces are only included in development mode.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


# =============================================================================
# Custom Exception Classes
# =============================================================================

class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500, detail: str | None = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class DuplicateException(AppException):
    """Duplicate resource detected."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} already exists: {identifier}",
            status_code=status.HTTP_409_CONFLICT,
        )


class ValidationException(AppException):
    """Input validation failed."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class FaceDetectionException(AppException):
    """Face detection or recognition related error."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class CameraException(AppException):
    """Camera access or streaming error."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class ModelException(AppException):
    """Model loading or inference error."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class DatabaseException(AppException):
    """Database operation error."""

    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


# =============================================================================
# Exception Handlers
# =============================================================================

def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI app."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.error(
            "Application error",
            error_type=type(exc).__name__,
            message=exc.message,
            status_code=exc.status_code,
            path=str(request.url),
        )
        content = {"error": exc.message, "status_code": exc.status_code}
        if settings.debug and exc.detail:
            content["detail"] = exc.detail
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled exception",
            error_type=type(exc).__name__,
            path=str(request.url),
        )
        # Never expose internal error details in production
        message = str(exc) if settings.debug else "Internal server error"
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": message, "status_code": 500},
        )

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Resource not found", "status_code": 404},
        )

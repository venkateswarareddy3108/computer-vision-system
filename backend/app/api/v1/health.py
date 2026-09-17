"""
Health check endpoints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "computer-vision-api"}

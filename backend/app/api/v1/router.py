"""
API v1 Router aggregation.
"""

from fastapi import APIRouter

from app.api.v1 import detection, health, persons, websocket

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router.include_router(detection.router, prefix="/detection", tags=["detection"])
api_router.include_router(websocket.router, tags=["websocket"])

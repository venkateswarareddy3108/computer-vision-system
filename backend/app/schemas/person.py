"""
Person-related Pydantic schemas for request validation and response serialization.

Designed to be extensible — additional_info (JSONB) allows arbitrary
application-specific fields without schema changes.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class PersonBase(BaseModel):
    """Shared person fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Full name")
    person_id: str = Field(..., min_length=1, max_length=50, description="Unique person/employee ID")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    department: Optional[str] = Field(None, max_length=255, description="Department")
    role: Optional[str] = Field(None, max_length=255, description="Role/position")
    additional_info: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Arbitrary extra fields (JSONB)",
    )

    @field_validator("person_id")
    @classmethod
    def validate_person_id(cls, v: str) -> str:
        """Person ID must be alphanumeric with optional hyphens/underscores."""
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Person ID cannot be empty")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        """Basic email format validation."""
        if v is not None and v.strip():
            v = v.strip().lower()
            if "@" not in v or "." not in v.split("@")[-1]:
                raise ValueError("Invalid email format")
        return v


class PersonCreate(PersonBase):
    """Schema for creating a new person (used with registration form)."""
    pass


class PersonUpdate(BaseModel):
    """Schema for updating person information. All fields optional."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=255)
    role: Optional[str] = Field(None, max_length=255)
    additional_info: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class PersonResponse(BaseModel):
    """Schema for person API responses. Never includes face embeddings."""

    id: UUID
    person_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)
    face_image_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    has_face_embedding: bool = False

    model_config = {"from_attributes": True}


class PersonListResponse(BaseModel):
    """Paginated person list response."""

    persons: List[PersonResponse]
    total: int
    page: int = 1
    per_page: int = 50


class RegistrationResponse(BaseModel):
    """Response after successful person registration with face embedding."""

    person: PersonResponse
    face_registered: bool
    message: str
    quality_score: Optional[float] = None

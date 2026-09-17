"""
Person API endpoints.
"""

from typing import Any
from uuid import UUID

import cv2
import numpy as np
from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.exceptions import ValidationException
from app.database.connection import get_session
from app.schemas.person import PersonCreate, PersonListResponse, PersonResponse, PersonUpdate, RegistrationResponse
from app.services.person_service import PersonService
from app.services.registration_service import RegistrationService
from app.utils.validators import validate_image_file

router = APIRouter()


@router.post("/", response_model=PersonResponse)
async def create_person(person_in: PersonCreate, session=Depends(get_session)):
    """Create a new person record (without face embedding)."""
    person_service = PersonService(session)
    person = await person_service.create_person(person_in)
    return person


@router.post("/{person_uuid}/face", response_model=RegistrationResponse)
async def register_face(
    person_uuid: UUID,
    file: UploadFile = File(...),
    replace_existing: bool = Form(False),
    session=Depends(get_session)
):
    """Register a face for a person."""
    validate_image_file(file)
    
    # Read image into memory
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValidationException("Failed to decode image")
        
    registration_service = RegistrationService(session)
    success, message, confidence = await registration_service.register_face(
        person_uuid=person_uuid,
        image_data=image,
        replace_existing=replace_existing
    )
    
    person_service = PersonService(session)
    person = await person_service.get_person_by_id(person_uuid)
    
    return RegistrationResponse(
        person=person,
        face_registered=success,
        message=message,
        quality_score=confidence
    )


@router.get("/", response_model=PersonListResponse)
async def get_persons(
    page: int = 1,
    per_page: int = 50,
    search: str = None,
    department: str = None,
    is_active: bool = None,
    session=Depends(get_session)
):
    """Get a paginated list of persons."""
    person_service = PersonService(session)
    persons, total = await person_service.get_persons(
        page=page, per_page=per_page, search=search, department=department, is_active=is_active
    )
    
    return PersonListResponse(
        persons=[PersonResponse.model_validate(p) for p in persons],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/{person_uuid}", response_model=PersonResponse)
async def get_person(person_uuid: UUID, session=Depends(get_session)):
    """Get a specific person by UUID."""
    person_service = PersonService(session)
    person = await person_service.get_person_by_id(person_uuid)
    return person


@router.patch("/{person_uuid}", response_model=PersonResponse)
async def update_person(
    person_uuid: UUID, person_update: PersonUpdate, session=Depends(get_session)
):
    """Update a person's information."""
    person_service = PersonService(session)
    person = await person_service.update_person(person_uuid, person_update)
    return person


@router.delete("/{person_uuid}")
async def delete_person(person_uuid: UUID, session=Depends(get_session)):
    """Delete a person."""
    person_service = PersonService(session)
    await person_service.delete_person(person_uuid)
    return {"status": "success", "message": "Person deleted"}

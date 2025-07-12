from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.schemas.appointment import (
    Appointment,
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentWithClient,
    AppointmentStatus
)
from app.schemas.common import PaginatedResponse
from app.db import models
from datetime import datetime, timedelta, date
from typing import Optional

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[AppointmentWithClient])
async def get_appointments(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[AppointmentStatus] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all appointments with pagination and filtering.
    - page: Page number (starts from 1)
    - page_size: Number of items per page
    - search: Search in client name
    - start_date: Filter appointments from this date (YYYY-MM-DD)
    - end_date: Filter appointments until this date (YYYY-MM-DD)
    - status: Filter by appointment status
    """
    query = db.query(models.Appointment).join(models.Client)
    
    # Apply date range filter if provided
    if start_date:
        # Convert date to datetime at start of day (00:00:00)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        query = query.filter(models.Appointment.time >= start_datetime)
    
    if end_date:
        # Convert date to datetime at end of day (23:59:59)
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(models.Appointment.time <= end_datetime)
    
    # Apply status filter if provided
    if status:
        query = query.filter(models.Appointment.status == status)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(models.Client.name.ilike(search_term))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = (total + page_size - 1) // page_size
    if page < 1:
        page = 1
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    # Get paginated results
    appointments = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": appointments,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }

@router.post("/", response_model=Appointment, status_code=201)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new appointment.
    """
    # Validate client exists
    client = db.query(models.Client).filter(models.Client.id == appointment.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Create in local database
    db_appointment = models.Appointment(
        client_id=client.id,
        time=appointment.time,
        status=appointment.status or AppointmentStatus.SCHEDULED,
        notes=appointment.notes
    )
    
    try:
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{appointment_id}", response_model=AppointmentWithClient)
async def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific appointment by ID.
    """
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/{appointment_id}", response_model=Appointment)
async def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an appointment.
    """
    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Update local database
    appointment_data = appointment_update.model_dump()
    try:
        for key, value in appointment_data.items():
            setattr(db_appointment, key, value)
        
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{appointment_id}")
async def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an appointment.
    """
    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id
    ).first()
    
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    try:
        db.delete(db_appointment)
        db.commit()
        return {"message": "Appointment deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
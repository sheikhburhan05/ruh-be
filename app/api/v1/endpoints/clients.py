from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.db.session import get_db
from app.schemas.client import Client, ClientWithAppointments, ClientCreate
from app.schemas.common import PaginatedResponse
from app.db import models

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[Client])
async def get_clients(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all clients with pagination and optional search.
    - page: Page number (starts from 1)
    - page_size: Number of items per page
    - search: Search in client name, email, and phone
    """
    # Base query
    query = db.query(models.Client)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Client.name.ilike(search_term),
                models.Client.email.ilike(search_term),
                models.Client.phone.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = (total + page_size - 1) // page_size
    if page < 1:
        page = 1
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    # Get paginated results
    clients = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "items": clients,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }

@router.get("/{client_id}", response_model=ClientWithAppointments)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific client by ID.
    """
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/{client_id}/appointments", response_model=PaginatedResponse[Client])
async def get_client_appointments(
    client_id: int,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get all appointments for a specific client with pagination.
    """
    # Check if client exists
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Get appointments query
    query = db.query(models.Appointment).filter(models.Appointment.client_id == client_id)
    
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

@router.post("/", response_model=Client)
async def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new client.
    """
    # Check if client with same email already exists
    existing_client = db.query(models.Client).filter(models.Client.email == client.email).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new client
    db_client = models.Client(
        name=client.name,
        email=client.email,
        phone=client.phone
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client 
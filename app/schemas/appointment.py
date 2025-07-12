from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class AppointmentBase(BaseModel):
    time: datetime
    status: AppointmentStatus
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    client_id: int

class AppointmentUpdate(AppointmentBase):
    time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Appointment(AppointmentBase):
    id: int
    client_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class AppointmentWithClient(Appointment):
    client: "Client"

    model_config = {
        "from_attributes": True
    }

from app.schemas.client import Client

AppointmentWithClient.model_rebuild() 
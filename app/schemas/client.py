from __future__ import annotations
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class ClientWithAppointments(Client):
    appointments: List["Appointment"] = []

    model_config = {
        "from_attributes": True
    }

from app.schemas.appointment import Appointment

ClientWithAppointments.model_rebuild() 
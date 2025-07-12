from fastapi import APIRouter
from app.api.v1.endpoints import clients, appointments

api_router = APIRouter()

api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"]) 
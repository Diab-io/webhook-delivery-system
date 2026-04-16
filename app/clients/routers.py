from app.clients.schemas import AppCreateRequest, AppCreateResponse, AppRead
from app.users.service import current_active_user
from app.users.models import User
from app.clients.services import get_app_service, AppService
from app.webhooks.schemas import WebhookResponse
from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

router = APIRouter()

@router.post('/', response_model=AppCreateResponse)
async def create_app(
    payload: AppCreateRequest,
    current_user: User = Depends(current_active_user),
    service: AppService = Depends(get_app_service)
):
    return await service.create_app(current_user, payload)

@router.get("/", response_model=List[AppRead])
async def get_user_apps(
    active: bool = True,
    current_user: User = Depends(current_active_user),
    service: AppService = Depends(get_app_service)
):
    return await service.get_user_apps(current_user, active)

@router.get("/{id}", response_model=AppRead)
async def get_user_app(
    id: UUID,
    current_user: User = Depends(current_active_user),
    service: AppService = Depends(get_app_service)
):
    return await service.get_user_app(current_user, id)

@router.get("/{id}/deactivate", response_model=AppRead)
async def deactivate_app(
    id: UUID,
    current_user: User = Depends(current_active_user),
    service: AppService = Depends(get_app_service)
):
    return await service.deactivate_app(current_user, id)

@router.get("/{id}/webhooks", response_model=List[WebhookResponse])
async def get_app_webhooks(
    id: UUID,
    current_user: User = Depends(current_active_user),
    service: AppService = Depends(get_app_service)
):
    return await service.get_app_webhooks(current_user, id)


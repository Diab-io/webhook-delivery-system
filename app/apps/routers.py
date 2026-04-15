from app.apps.schemas import AppCreateRequest, AppCreateResponse, AppRead
from app.users.service import current_active_user
from app.users.models import User
from app.apps.services import get_app_service, AppService
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter()

@router.post('/apps', response_model=AppCreateResponse)
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



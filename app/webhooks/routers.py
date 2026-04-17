from fastapi import APIRouter, Depends
from app.webhooks.schemas import WebhookUpdateRequest, WebhookResponse
from uuid import UUID
from app.users.models import User
from app.users.service import current_active_user
from app.webhooks.services import get_webhook_service, WebhookService

router = APIRouter()

@router.patch('/{id}', response_model=WebhookResponse)
async def update_webhook(
    id: UUID,
    payload: WebhookUpdateRequest,
    current_user: User = Depends(current_active_user),
    service: WebhookService = Depends(get_webhook_service),
):
    return await service.update_webhook(current_user, id, payload)

@router.post('/{id}/deactivate', response_model=WebhookResponse)
async def deactivate_webhook(
    id: UUID,
    current_user: User = Depends(current_active_user),
    service: WebhookService = Depends(get_webhook_service)
):
    return await service.set_webhook_state(current_user, id, active=False)

@router.post('/{id}/activate', response_model=WebhookResponse)
async def activate_webhook(
    id: UUID,
    current_user: User = Depends(current_active_user),
    service: WebhookService = Depends(get_webhook_service)
):
    return await service.set_webhook_state(current_user, id, active=True)

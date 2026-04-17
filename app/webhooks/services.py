from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.webhooks.models import Webhook
from app.webhooks.schemas import WebhookCreateRequest, WebhookUpdateRequest
from app.clients.services import AppService
from app.clients.models import App
from app.core.exceptions import AppNotActive, WebhookNotFound
from app.users.models import User
from app.core.security.secrets import generate_webhook_secret
from app.core.database import get_async_session
from app.core.security.encryption import encrypt
from uuid import UUID
from typing import Dict, Any
from fastapi import Depends


class WebhookService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._model = Webhook
        
    async def user_owns_webhook(self, current_user: User, webhook_id: UUID) -> Webhook | None:
        stmt = (
            select(Webhook)
            .join(App)
            .where(
                Webhook.id == webhook_id,
                App.user_id == current_user.id
            )
        )

        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def register_webhook(
            self,
            payload: WebhookCreateRequest,
            current_user: User,
            app_service: AppService,
            app_id: UUID
    ) -> Dict[str, Any]:
        app = await app_service.get_user_owned_app(current_user, app_id)

        if not app.active:
            raise AppNotActive(app.id)
        
        webhook_secret = generate_webhook_secret()
        encrypted_webhook_secret = encrypt(webhook_secret)

        dump = payload.model_dump()
        dump['url'] = str(dump['url'])

        new_webhook = self._model(
            **dump,
            secret_key=encrypted_webhook_secret,
            app_id=app_id
        )  

        self._db.add(new_webhook)
        await self._db.commit()
        await self._db.refresh(new_webhook)

        return {
            "id": new_webhook.id,
            "url": new_webhook.url,
            "app_id": new_webhook.app_id,
            "active": True,
            "secret_key": webhook_secret
        }     
    
    async def update_webhook(self, current_user: User, webhook_id: UUID, payload: WebhookUpdateRequest) -> Webhook:
        webhook = await self.user_owns_webhook(current_user, webhook_id)

        if webhook is None:
            raise WebhookNotFound(webhook_id)
        
        allowed_fields = {"url"}
        for key, value in payload.model_dump(exclude_unset=True).items():
            if key in allowed_fields:
                setattr(webhook, key, value)
        
        await self._db.commit()
        await self._db.refresh(webhook)

        return webhook
    
    async def set_webhook_state(self, current_user: User, webhook_id: UUID, active: bool = True) -> Webhook:
        webhook = await self.user_owns_webhook(current_user, webhook_id)

        if webhook is None:
            raise WebhookNotFound(webhook_id)
        
        webhook.active = active
        
        await self._db.commit()
        await self._db.refresh(webhook)

        return webhook
    
    async def get_app_webhooks(self, current_user: User, app_service: AppService, app_id: UUID):
        await app_service.get_user_owned_app(current_user, app_id)
        query = select(Webhook).where(Webhook.app_id == app_id)
        result = await self._db.execute(query)
        return result.scalars().all()


def get_webhook_service(db: AsyncSession = Depends(get_async_session)) -> WebhookService:
    return WebhookService(db)

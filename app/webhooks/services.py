from sqlalchemy.ext.asyncio import AsyncSession
from app.webhooks.models import Webhook
from app.webhooks.schemas import WebhookCreateRequest
from app.clients.services import AppService
from app.core.exceptions import AppNotActive
from app.users.models import User
from app.core.security.secrets import generate_webhook_secret
from app.core.security.encryption import encrypt
from uuid import UUID

class WebhookService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self.model = Webhook
    
    async def register_webhook(
            self,
            payload: WebhookCreateRequest,
            current_user: User,
            app_service: AppService,
            app_id: UUID
    ):
        app = await app_service.get_user_owned_app(current_user, app_id)

        if not app.active:
            raise AppNotActive(app.id)
        
        webhook_secret = generate_webhook_secret()
        encrypted_webhook_secret = encrypt(webhook_secret)

        new_webhook = self.model(
            **payload.model_dump(),
            secret_key=encrypted_webhook_secret
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


        


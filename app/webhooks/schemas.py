from pydantic import BaseModel, AnyHttpUrl
from uuid import UUID
from typing import Optional


class WebhookCreateRequest(BaseModel):
    url: AnyHttpUrl
    app_id: UUID

class WebhookResponse(BaseModel):
    id: UUID
    app_id: UUID
    url: AnyHttpUrl
    active: bool

class WebhookCreateResponse(WebhookResponse):
    secret_key: str

class WebhookUpdateRequest(BaseModel):
    url: Optional[AnyHttpUrl] = None

class WebhookDeleteRequest(BaseModel):
    webhook_id: UUID

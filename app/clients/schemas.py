from pydantic import BaseModel
from uuid import UUID


class AppRead(BaseModel):
    id: UUID
    name: str
    active: bool

class AppCreateRequest(BaseModel):
    name: str
    event_type_field: str | None = None
    payload_field: str |  None = None
    event_id_field: str | None = None

class AppCreateResponse(AppCreateRequest):
    api_key: str
    active: bool

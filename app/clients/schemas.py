from pydantic import BaseModel
from uuid import UUID


class AppRead(BaseModel):
    id: UUID
    name: str
    active: bool

class AppCreateRequest(BaseModel):
    name: str

class AppCreateResponse(AppCreateRequest):
    api_key: str
    active: bool

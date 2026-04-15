from pydantic import BaseModel
from uuid import UUID


class AppRead(BaseModel):
    id: UUID
    name: str

class AppCreateRequest(BaseModel):
    name: str

class AppCreateResponse(AppCreateRequest):
    api_key: str

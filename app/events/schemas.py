from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from uuid import UUID


class EventTriggerRequest(BaseModel):
    event_type: str
    event_id: Optional[str] = None
    source: Optional[str] = None
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    occurred_at: Optional[datetime] = None

    @field_validator("occured_at")
    def ensure_utc(cls, value: datetime):
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

class EventResponseResponse(BaseModel):
    id: UUID
    app_id: UUID
    event_type: str
    event_id: Optional[str] = None
    source: Optional[str] = None
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    occurred_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

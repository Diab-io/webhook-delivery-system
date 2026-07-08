from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, JSON, DateTime, Enum, UniqueConstraint
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import enum


class EventDeliveryEnum(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    app_id: Mapped[UUID] = mapped_column(ForeignKey("apps.id"))
    event_type: Mapped[str] = mapped_column(nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    external_event_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
    
    __table_args__ = (
        UniqueConstraint('app_id', 'external_event_id', name='uq_app_external_event'),
    )
    

class WebhookEventSubscription(Base):
    __tablename__ = "webhook_event_subscription"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    webhook_id: Mapped[UUID] = mapped_column(ForeignKey("webhooks.id"))
    event_type: Mapped[str]


class EventDelivery(Base):
    __tablename__ = "events_deliveries"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"))
    webhook_id: Mapped[UUID] = mapped_column(ForeignKey('webhooks.id'))
    status: Mapped[EventDeliveryEnum] = mapped_column(Enum(EventDeliveryEnum),
                                                      default=EventDeliveryEnum.PENDING, nullable=False)
    attempt_count: Mapped[int] = mapped_column(default=0)
    last_attempt_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    response_status: Mapped[Optional[int]] = mapped_column(nullable=True)
    response_body: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)

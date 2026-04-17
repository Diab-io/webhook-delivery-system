from uuid import uuid4, UUID
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, DateTime
from datetime import datetime, timezone
from typing import List

class App(Base):
    __tablename__ = 'apps'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str]
    api_key_prefix: Mapped[str] = mapped_column(unique=True, index=True)
    api_key: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="apps")
    webhooks: Mapped[List["Webhook"]] = relationship(back_populates="app")

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uq_app_name_user'),
    )

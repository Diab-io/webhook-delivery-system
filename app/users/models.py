from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    apps: Mapped[List["App"]] = relationship(back_populates="user")
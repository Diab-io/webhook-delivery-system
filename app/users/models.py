from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
import secrets
import bcrypt
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from app.users.models import User
from app.apps.models import App
from app.apps.schemas import AppCreateRequest
from app.core.exceptions import DuplicateUserApp, AppNotFound, NotAppOwner
from app.core.database import get_async_session
from typing import Dict, Any, Optional, List
from uuid import UUID


class AppService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self.model = App
    
    def generate_api_key(self) -> str:
        return secrets.token_urlsafe(16)
    
    def hash_api_key(self, api_key: str) -> str:
        return bcrypt.hashpw(api_key.encode, bcrypt.gensalt()).decode()
    
    def verify_api_key(self, plain_key: str, hashed_key: str) -> bool:
        return bcrypt.checkpw(plain_key.encode(), hashed_key.encode())
    
    async def execute_query(self, query: Executable) -> Result:
        result = await self._db.execute(query)
        return result
    
    async def create_app(self, current_user: User, payload: AppCreateRequest) -> Dict[str, Any]:
        app_name = payload.name

        query = select(self.model).where(
            self.model.name == app_name,
            self.model.user_id == current_user.id
        )
        result = await self.execute_query(query)
        existing_app = result.scalars().first()

        if existing_app:
            raise DuplicateUserApp()
        
        plain_api_key = self.generate_api_key()

        hashed_api_key = self.hash_api_key(plain_api_key)

        new_app = self.model(**payload.model_dump(), user_id=current_user.id, api_key=hashed_api_key)
        self._db.add(new_app)
        await self._db.commit()
        await self._db.refresh(new_app)

        return {
            "id": new_app.id,
            "name": new_app.name,
            "api_key": plain_api_key
        }
    
    async def get_user_apps(self, current_user: User, active: bool) -> Optional[List[App]]:
        query = select(self.model).where(
            self.model.user_id == current_user.id,
            self.model.active == active
        )
        result = await self.execute_query(query)
        return result.scalars()
    
    async def get_user_app(self, current_user: User, app_id: UUID):
        app = await self.model.get(app_id)

        if not app:
            raise AppNotFound(app_id)
        
        user_id = current_user.id
        if app.user_id != user_id:
            raise NotAppOwner(user_id, app_id)
        
        return app
    


def get_app_service(db: AsyncSession = Depends(get_async_session)) -> AppService:
    return AppService(db)

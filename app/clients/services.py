from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from app.users.models import User
from app.clients.models import App
from app.clients.schemas import AppCreateRequest
from app.core.security.secrets import generate_api_key, hash_api_key
from app.core.exceptions import DuplicateUserApp, AppNotFound, NotAppOwner
from app.core.database import get_async_session
from typing import Dict, Any, Optional, List
from uuid import UUID


class AppService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self.model = App
    
    async def get_app_by_id(self, id: UUID) -> str:
        return await self._db.get(self.model, id)
    
    async def execute_query(self, query: Executable) -> Result:
        result = await self._db.execute(query)
        return result
    
    async def get_user_owned_app(self, current_user: User, app_id: UUID) -> App:
        app = await self.get_app_by_id(app_id)

        if not app:
            raise AppNotFound(app_id)
        
        if app.user_id != current_user.id:
            raise NotAppOwner(current_user.id, app_id)
        
        return app
    
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
        
        plain_api_key = generate_api_key()
        api_key_prefix = plain_api_key.split('.', 1)[0]

        hashed_api_key = hash_api_key(plain_api_key)

        new_app = self.model(
            **payload.model_dump(),
            user_id=current_user.id,
            api_key=hashed_api_key,
            api_key_prefix=api_key_prefix
        )
        self._db.add(new_app)
        await self._db.commit()
        await self._db.refresh(new_app)

        return {
            "id": new_app.id,
            "name": new_app.name,
            "api_key": plain_api_key,
            "active": new_app.active
        }
    
    async def get_user_apps(self, current_user: User, active: bool) -> Optional[List[App]]:
        query = select(self.model).where(
            self.model.user_id == current_user.id,
            self.model.active == active
        )
        result = await self.execute_query(query)
        return result.scalars()
    
    async def get_user_app(self, current_user: User, app_id: UUID) -> App:
        return await self.get_user_owned_app(current_user, app_id)
    
    async def deactivate_app(self, current_user: User, app_id: UUID) -> App:
        app = await self.get_user_owned_app(current_user, app_id)
        app.active = False

        await self._db.commit()
        await self._db.refresh(app)

        return app
    
    async def get_app_webhooks(self, current_user: User, app_id: UUID):
        stmt = (
            select(App)
            .options(selectinload(App.webhooks))
            .where(
                App.id == app_id,
                App.user_id == current_user.id
            )
        )

        result = await self.execute_query(stmt)
        app = result.scalar_one_or_none()

        if app is None:
            raise AppNotFound(app_id)
        
        return app.webhooks


def get_app_service(db: AsyncSession = Depends(get_async_session)) -> AppService:
    return AppService(db)

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from uuid import UUID

class DuplicateUserApp(Exception):
    pass


class AppNotFound(Exception):
    def __init__(self, app_id: UUID):
        self.app_id = app_id


class NotAppOwner(Exception):
    def __init__(self, user_id: UUID, app_id: UUID):
        self.user_id = user_id
        self.app_id = app_id


class AppNotActive(Exception):
    def __init__(self, app_id: UUID):
        self.app_id = app_id


class WebhookNotFound(Exception):
    def __init__(self, webhook_id: UUID):
        self.webhook_id = webhook_id


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(DuplicateUserApp)
    async def duplicate_user_app_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "DUPLICATE_USER_APP"}
        )
    
    @app.exception_handler(AppNotFound)
    async def app_not_found_handler(request, exc):
        app_id = exc.app_id

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": "APP_NOT_FOUND",
                "app_id": app_id
            }
        )
    
    @app.exception_handler(NotAppOwner)
    async def not_app_owner_handler(request, exc):
        user_id = exc.user_id
        app_id = exc.app_id

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": "NOT_APP_OWNER",
                "app_id": app_id,
                "user_id": user_id
            }
        )
    
    @app.exception_handler(AppNotActive)
    async def app_not_active_handler(request, exc):
        app_id = exc.app_id

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "APP_NOT_ACTIVE",
                "app_id": app_id,
            }
        )
    
    @app.exception_handler(WebhookNotFound)
    async def webhook_not_found_handler(request, exc):
        webhook_id = exc.webhook_id

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": "WEBHOOK_NOT_FOUND",
                "webhook_id": webhook_id,
            }
        )

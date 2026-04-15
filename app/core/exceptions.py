from fastapi import FastAPI
from fastapi.responses import JSONResponse
from uuid import UUID

class DuplicateUserApp(Exception):
    pass

class AppNotFound(Exception):
    def __init__(self, app_id: UUID):
        self.app_id = app_id


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(DuplicateUserApp)
    async def duplicate_user_app_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": "DUPLICATE_USER_APP"}
        )
    
    @app.exception_handler(AppNotFound)
    async def app_not_found_handler(request, exc):
        app_id = exc.app_id

        return JSONResponse(
            status_code=404,
            content={
                "detail": "APP_NOT_FOUND",
                "app_id": app_id
            }
        )

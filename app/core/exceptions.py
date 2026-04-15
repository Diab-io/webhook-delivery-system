from fastapi import FastAPI
from fastapi.responses import JSONResponse

class DuplicateUserApp(Exception):
    pass


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(DuplicateUserApp)
    async def duplicate_user_app_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": "DUPLICATE_USER_APP"}
        )

from fastapi import Depends, FastAPI

from app.users.models import User
from app.users.schemas import UserCreate, UserRead, UserUpdate
from app.users.service import auth_backend, current_active_user, fastapi_users
from app.core.exceptions import register_exception_handlers
from app.clients.routers import router as client_route


app = FastAPI()
register_exception_handlers(app)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/api/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/users",
    tags=["users"],
)
app.include_router(
    client_route,
    prefix="/api/apps",
    tags=["Apps"],
)



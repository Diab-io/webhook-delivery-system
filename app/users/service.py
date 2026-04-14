import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from app.core.dependencies import get_user_db
from app.users.models import User
from app.core.mail import send_email
from app.core.settings import JWT_SECRET



class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = JWT_SECRET
    verification_token_secret = JWT_SECRET
    
    async def on_after_request_verify(self, user, token, request = None):
        verify_link = f"{request.base_url}/verify?token={token}"

        await send_email(
            template_name="verify_email.html",
            subject="Verify Your Email",
            recipients=[user.email],
            context={
                "user_email": user.email,
                "verify_link": verify_link,
                "user_name": user.username
            }
        )

    # async def on_after_forgot_password(
    #     self, user: User, token: str, request: Request | None = None
    # ):
    #     reset_link = f"http://{request.base_url}/reset-password?token={token}"

    #     await send_email(
    #         template_name="reset_password.html",
    #         subject="Reset Your Password",
    #         recipients=[user.email],
    #         context={
    #             "user_email": user.email,
    #             "reset_link": reset_link,
    #             "user_name": user.username
    #         }
    #     )

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
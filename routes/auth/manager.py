from fastapi_users import BaseUserManager, UUIDIDMixin
from database.connection import get_user_db
from models.user import User
from fastapi import Depends, Request, Response
from .libs import SECRET
import uuid
from typing import Optional

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        
    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        response = await super().on_after_login(user, request, response)
        print(response)
        return response

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
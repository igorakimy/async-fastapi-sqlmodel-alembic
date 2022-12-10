from typing import List

from pydantic import ValidationError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.core.config import settings
from app.models.user import User
from app.schemas.user import IUserRead, IUserCreate
from app.exceptions.credentials import InvalidCredentialsException
from app.exceptions.users import (
    UserInactiveException,
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.api.v1.deps.db import bind_repo
from app.exceptions.roles import InvalidRoleException
from app.db.repositories.user import UserRepository


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/login/token"
)


def get_current_user(required_roles: List[str] = None):
    async def current_user(
        token: str = Depends(reusable_oauth2),
        user_repo: UserRepository = Depends(bind_repo(UserRepository, User))
    ) -> User:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id: str = payload["sub"]
            if user_id is None:
                raise InvalidCredentialsException()
        except (jwt.JWTError, ValidationError):
            raise InvalidCredentialsException()

        user: User = await user_repo.get(id=user_id)

        if not user:
            raise UserNotFoundException()

        if not user.is_active:
            raise UserInactiveException()

        if required_roles:
            if not any(role == user.role.slug for role in required_roles):
                roles = ("'" + role + "'" for role in required_roles)
                msg = f"Следующие роли требуются для этого действия: {', '.join(roles)}"
                raise InvalidRoleException(msg)

        return user

    return current_user


async def user_exists(
    new_user: IUserCreate,
    user_repo: UserRepository
) -> IUserCreate:
    user = await user_repo.get_by_email(email=new_user.email)
    if user:
        msg = "Уже существует пользователь с таким email"
        raise UserAlreadyExistsException(msg)
    return new_user


async def is_valid_user(
    user_id: int,
    user_repo: UserRepository
) -> IUserRead:
    user: IUserRead = await user_repo.get(id=user_id)
    if not user:
        raise UserNotFoundException()
    return user

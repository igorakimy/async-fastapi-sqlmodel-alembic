from datetime import timedelta
from typing import Any, Optional

from pydantic import EmailStr
from fastapi import APIRouter, Body, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core import security
from app.schemas.common import IMetaGeneral
from app.schemas.response import IPostResponseBase, response
from app.schemas.common import TokenType
from app.schemas.token import Token, TokenRead
from app.models.user import User
from app.api.v1.deps import meta
from app.exceptions import (
    InvalidEmailOrPasswordException,
    InvalidTokenException,
    UserInactiveException,
    UserNotFoundException,
)
from app.api.v1.deps import bind_repo
from app.utils.encryptor import (
    generate_password_reset_token,
    verify_password_reset_token,
)
from app.utils.mailer import send_password_reset_mail
from app.db.repositories.user import UserRepository


router = APIRouter()


@router.post("", response_model=IPostResponseBase[Token])
async def login(
    email: EmailStr = Body(...),
    password: str = Body(...),
    meta_data: IMetaGeneral = Depends(meta.get_general_meta),
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User)),
) -> Any:
    """
    Login for all users
    """

    user = await user_repo.authenticate(
        email=email,
        password=password
    )
    if not user:
        raise InvalidEmailOrPasswordException()
    elif not user.is_active:
        raise UserInactiveException()

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token_expires = timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_token(
        user.id,
        TokenType.access,
        expires_delta=access_token_expires
    )
    refresh_token = security.create_token(
        user.id,
        TokenType.refresh,
        expires_delta=refresh_token_expires
    )
    data = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user=user
    )

    return response(
        meta=meta_data,
        data=data,
        message="Login correctly"
    )


@router.post("/token", response_model=TokenRead)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User))
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await user_repo.authenticate(
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise InvalidEmailOrPasswordException()
    elif not user.is_active:
        raise UserInactiveException()

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_token(
        user.id,
        TokenType.access,
        expires_delta=access_token_expires
    )

    return TokenRead(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/password-recovery/{email}")
async def recover_password(
    email: str,
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User))
) -> Any:
    """
    Password recovery
    """
    print(email)
    user: User = await user_repo.get_by_email(email=email)
    if not user:
        raise UserNotFoundException()
    password_reset_token = generate_password_reset_token(email=email)
    send_password_reset_mail(
        email_to=user.email,
        email=email,
        token=password_reset_token
    )
    return {"detail": "Password recovery email sent"}


@router.post("/reset-password")
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User))
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise InvalidTokenException()
    user = await user_repo.get_by_email(email=email)
    if not user:
        raise UserNotFoundException()
    elif not user_repo.is_active(user):
        raise UserInactiveException()
    await user_repo.update_password(
        user,
        new_password
    )
    return {"detail": "Password updated successfully"}

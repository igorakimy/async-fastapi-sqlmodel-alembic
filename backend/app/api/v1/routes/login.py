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
    UserInactiveException,
)
from app.api.v1.deps import bind_repo
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

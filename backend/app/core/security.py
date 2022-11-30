from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from .config import settings
from app.schemas.common import TokenType


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def create_token(
    subject: Union[str, Any],
    token_type: TokenType,
    expires_delta: timedelta = None
) -> str:
    """
    Create new access or refresh token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        const_name = f"{token_type.upper()}_TOKEN_EXPIRE_MINUTES"
        expire = datetime.utcnow() + timedelta(
            minutes=getattr(settings, const_name)
        )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": token_type
    }
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.JWT_ALGORITHM
    )


def get_password_hash(password: Union[str, int]) -> str:
    """
    Get hashed password.
    """
    return password_context.hash(str(password))


def verify_password(
    plain_password: Union[str, int],
    hashed_password: str
) -> bool:
    """
    Verify password with hashed password.
    """
    return password_context.verify(
        str(plain_password),
        hashed_password
    )

from typing import (
    Any,
    Dict,
    Optional,
)

from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):

    def __init__(
        self,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
            headers=headers
        )


class InvalidEmailOrPasswordException(HTTPException):

    def __init__(
        self,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message or "Email or Password incorrect",
            headers=headers
        )


class InvalidTokenException(HTTPException):

    def __init__(
        self,
        message: Optional[str] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message or "Invalid token"
        )

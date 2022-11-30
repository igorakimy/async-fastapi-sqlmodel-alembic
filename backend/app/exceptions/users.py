from typing import (
    Optional,
    Dict,
    Any,
)

from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):

    def __init__(self, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message or "User not found"
        )


class UserInactiveException(HTTPException):

    def __init__(self, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message or "Inactive user"
        )


class UserAlreadyExistsException(HTTPException):

    def __init__(self, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message or "User already exists"
        )


class UserSelfDeleteException(HTTPException):

    def __init__(
        self,
        message: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message or "Users can not delete themselves",
            headers=headers
        )

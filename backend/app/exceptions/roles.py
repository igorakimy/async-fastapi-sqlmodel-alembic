from typing import Optional

from fastapi import HTTPException, status

from app.models.role import Role


class InvalidRoleException(HTTPException):

    def __init__(self, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message or "Access denied"
        )


class RoleNotFoundException(HTTPException):

    def __init__(
        self,
        role: Optional[Role] = None,
        message: Optional[str] = None,
    ):
        role_name = ' ' + role.name if role else ''
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message or f"Role{role_name} not found"
        )

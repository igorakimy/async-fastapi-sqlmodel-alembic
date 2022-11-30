from enum import Enum
from typing import Optional

from pydantic import validator

from app.utils.partial import optional
from app.models.user import UserBase
from .role import IRoleRead


class IUserCreate(UserBase):
    password: str
    password_repeat: str

    @validator('password_repeat', always=True)
    def password_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    class Config:
        password = "Main"


@optional
class IUserUpdate(UserBase):
    pass


class IUserRead(UserBase):
    id: int
    role: Optional[IRoleRead]


class IUserStatus(str, Enum):
    active = "active"
    inactive = "inactive"

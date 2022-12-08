from enum import Enum
from typing import Optional

from pydantic import validator

from app.utils.partial import optional
from app.models.user import UserBase
from .role import IRoleRead


class IUserCreate(UserBase):
    password: str
    password_confirmation: str

    @validator('password_confirmation', always=True)
    def password_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    class Config:
        password = "Main"


@optional
class IUserUpdate(UserBase):
    password: Optional[str] = None
    password_confirmation: Optional[str] = None

    @validator("password_confirmation", always=True)
    def password_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v


class IUserRead(UserBase):
    id: int
    role: Optional[IRoleRead]


class IUserStatus(str, Enum):
    active = "active"
    inactive = "inactive"

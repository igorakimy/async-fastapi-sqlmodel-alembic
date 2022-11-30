from typing import Optional

from pydantic import EmailStr
from sqlmodel import (
    Field,
    SQLModel,
    Relationship,
)

from app.models.base import BaseModel


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr = Field(
        nullable=False,
        index=True,
        sa_column_kwargs={"unique": True}
    )
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")


class User(BaseModel, UserBase, table=True):
    password: Optional[str] = Field(nullable=False)
    role: Optional["Role"] = Relationship(
        back_populates="users",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

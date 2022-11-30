from typing import List

from sqlmodel import SQLModel, Relationship

from app.models.base import BaseModel


class RoleBase(SQLModel):
    name: str
    slug: str
    description: str


class Role(BaseModel, RoleBase, table=True):
    users: List["User"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel as _SQLModel, Field
from sqlalchemy.orm import declared_attr


class SQLModel(_SQLModel):

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class BaseModel(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True, nullable=False)
    created_at: Optional[datetime] = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=datetime.now())

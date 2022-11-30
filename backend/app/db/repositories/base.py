from typing import Type

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CrudBase


class BaseRepository(CrudBase):
    def __init__(
        self,
        model: Type[SQLModel],
        db: AsyncSession
    ):
        super().__init__(model, db)

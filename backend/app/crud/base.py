from datetime import datetime
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union
)

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.async_sqlmodel import paginate
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination import Params
from sqlmodel import SQLModel, select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select

from app.schemas.common import IOrderEnum


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

    def __init__(
        self,
        model: Type[ModelType],
        db: Optional[AsyncSession] = None
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    async def all(self) -> List[ModelType]:
        response = await self.db.execute(select(self.model))
        return response.scalars().all()

    async def get(
        self,
        *,
        id: Union[int, str]
    ) -> Optional[ModelType]:
        """
        Get entity by ID.
        """
        response = await self.db.execute(
            select(self.model).where(self.model.id == int(id))
        )
        return response.scalar_one_or_none()

    async def get_by_ids(
        self,
        *,
        list_ids: List[Union[int, str]]
    ) -> Optional[List[ModelType]]:
        """
        Get multiple entities by list of IDs.
        """
        response = await self.db.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_by_field(
        self,
        field_name: str,
        field_value: Union[int, str, bool]
    ) -> Optional[ModelType]:
        """
        Get entity by field.
        """
        response = await self.db.execute(
            select(self.model)
            .where(getattr(self.model, field_name) == field_value)
        )
        return response.scalar_one()

    async def get_count(self) -> Optional[ModelType]:
        response = await self.db.execute(
            select(func.count()).select_from(
                select(self.model).subquery()
            )
        )
        return response.scalar_one()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: Optional[Union[T, Select[T]]] = None
    ) -> List[ModelType]:
        if query is None:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(self.model.id)
            )
        response = await self.db.execute(query)
        return response.scalars().all()

    async def get_multi_ordered(
        self,
        *,
        order_by: Optional[str] = None,
        order: Optional[IOrderEnum] = IOrderEnum.ascending,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        columns = self.model.__table__.columns

        if order_by not in columns or order_by in None:
            order_by = self.model.id

        query = (
            select(self.model)
            .offset(skip)
            .limit(limit)
        )

        if order == IOrderEnum.ascending:
            query = query.order_by(columns[order_by.name].asc())
        else:
            query = query.order_by(columns[order_by.name].desc())

        response = await self.db.execute(query)
        return response.scalars().all()

    async def get_multi_paginated_ordered(
        self,
        *,
        params: Optional[Params] = Params(),
        order_by: Optional[str] = None,
        order: Optional[IOrderEnum] = IOrderEnum.ascending,
        query: Optional[Union[T, Select[T]]] = None
    ) -> AbstractPage[ModelType]:
        """
        Get multiple entities with pagination and ordering.
        """
        columns = self.model.__table__.columns

        if order_by is None or order_by not in columns:
            order_by = self.model.id

        if query is None:
            if order == IOrderEnum.ascending:
                query = (
                    select(self.model)
                    .order_by(columns[order_by.name].asc())
                )
            else:
                query = (
                    select(self.model)
                    .order_by(columns[order_by.name].desc())
                )

        return await paginate(self.db, query, params)

    async def create(
        self,
        *,
        entity: Union[CreateSchemaType, ModelType]
    ) -> ModelType:
        """
        Create new entity.
        """
        db_obj = self.model.from_orm(entity)

        if hasattr(db_obj, self.CREATED_AT):
            setattr(db_obj, self.CREATED_AT, datetime.utcnow())
        if hasattr(db_obj, self.UPDATED_AT):
            setattr(db_obj, self.UPDATED_AT, datetime.utcnow())

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        *,
        model: ModelType,
        data: Union[UpdateSchemaType, Dict[str, Any], ModelType]
    ) -> ModelType:
        obj_data = jsonable_encoder(model)

        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(model, field, update_data[field])
            if field == self.UPDATED_AT:
                setattr(model, field, datetime.utcnow())

        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def delete(self, *, id: Union[int, str]) -> ModelType:
        """
        Deleting by ID.
        """
        response = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        deleting_obj = response.scalar_one()
        await self.db.delete(deleting_obj)
        await self.db.commit()
        return deleting_obj

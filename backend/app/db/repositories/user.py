from datetime import datetime
from typing import Optional, List, Union

from fastapi.encoders import jsonable_encoder
from sqlmodel import select

from app.models.user import User
from app.schemas.user import (
    IUserRead,
    IUserCreate,
    IUserUpdate
)
from app.core.security import get_password_hash, verify_password
from .base import BaseRepository


class UserRepository(BaseRepository):

    async def get_by_email(
        self,
        *,
        email: str
    ) -> Optional[User]:
        users = await self.db.execute(
            select(User).where(User.email == email)
        )
        return users.scalar_one_or_none()

    async def authenticate(
        self,
        *,
        email: str,
        password: str
    ) -> Optional[User]:
        user = await self.get_by_email(email=email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    async def create_with_role(
        self,
        *,
        data: IUserCreate
    ) -> User:
        db_obj = self.model.from_orm(data)
        db_obj.password = get_password_hash(data.password)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update_password(self, user: User, new_password: str) -> User:
        user.password = get_password_hash(new_password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_with_role(
        self,
        *,
        model: User,
        data: IUserUpdate
    ) -> User:
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

        if 'password' in update_data:
            model.password = get_password_hash(update_data['password'])

        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    def is_active(self, user: User) -> bool:
        return user.is_active

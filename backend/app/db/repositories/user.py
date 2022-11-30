from typing import Optional, List

from sqlmodel import select

from app.models.user import User
from app.schemas.user import IUserCreate
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

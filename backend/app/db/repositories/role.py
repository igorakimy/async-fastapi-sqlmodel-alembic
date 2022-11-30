from typing import Optional

from sqlmodel import select

from .base import BaseRepository
from app.models.role import Role


class RoleRepository(BaseRepository):

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        response = await self.db.execute(
            select(self.model).where(self.model.name == name)
        )
        return response.scalar_one_or_none()

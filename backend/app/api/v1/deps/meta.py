from fastapi import Depends

from app.api.v1.deps.db import bind_repo
from app.schemas.common import IMetaGeneral
from app.db.repositories.role import RoleRepository
from app.models.role import Role


async def get_general_meta(
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role))
) -> IMetaGeneral:
    current_roles = await role_repo.get_multi()
    return IMetaGeneral(roles=current_roles)

import logging

from fastapi import Depends

from app.api.v1.deps.db import bind_repo
from app.schemas.content.users import users
from app.schemas.content.roles import roles
from app.models.role import Role
from app.models.user import User
from app.db.repositories.role import RoleRepository
from app.db.repositories.user import UserRepository


logger = logging.getLogger(__name__)


async def create_roles_task(
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role))
) -> None:
    for role in roles:
        role_current = await role_repo.get_role_by_name(
            name=role.slug
        )
        if not role_current:
            await role_repo.create(entity=role)


async def create_users_task(
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User)),
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role)),
) -> None:
    for user in users:
        current_user = await user_repo.get_by_email(
            email=user["data"].email
        )
        role = await role_repo.get_role_by_name(
            name=user["role"]
        )
        if not current_user:
            user["data"].role_id = role.id
            await user_repo.create_with_role(
                data=user["data"]
            )


async def exec_all_tasks() -> None:
    await create_roles_task()
    await create_users_task()

from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.role import (
    IRoleRead,
    IRoleEnum,
    IRoleCreate,
    IRoleUpdate,
)
from app.models.role import Role
from app.models.user import User
from app.api.v1.deps import bind_repo, get_current_user
from app.exceptions import (
    RoleSelfDeleteException,
    RoleNotFoundException,
)
from app.db.repositories import (
    RoleRepository,
)


router = APIRouter()


@router.get("", response_model=List[IRoleRead])
async def get_roles(
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role))
):
    roles = await role_repo.get_multi()
    return roles


@router.get("/{id}", response_model=IRoleRead)
async def get_one_role(
    id: int,
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role))
):
    role = await role_repo.get(id=id)
    if not role:
        raise RoleNotFoundException()
    return role


@router.post("", response_model=IRoleRead, status_code=status.HTTP_201_CREATED)
async def create_new_role(
    request_data: IRoleCreate,
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role))
):
    new_role = await role_repo.create(entity=request_data)
    return new_role


@router.put("/{id}", response_model=IRoleRead)
async def update_role(
    id: int,
    request_data: IRoleUpdate,
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role))
):
    updating_role = await role_repo.get(id=id)
    if not updating_role:
        raise RoleNotFoundException()
    updated_role = await role_repo.update(
        model=updating_role,
        data=request_data,
    )
    return updated_role


@router.delete("/{id}", response_model=IRoleRead)
async def delete_role(
    id: int,
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role)),
    current_user: User = Depends(get_current_user(required_roles=[
        IRoleEnum.admin
    ]))
):
    if current_user.role.id == id:
        raise RoleSelfDeleteException()
    deleted_role = await role_repo.delete(id=id)
    return deleted_role

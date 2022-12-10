from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

from app.schemas.response import (
    response,
    IGetResponseBase,
    IPostResponseBase,
    IPutResponseBase,
    IDeleteResponseBase,
    IGetResponsePaginated,
)
from app.schemas.user import (
    IUserRead,
    IUserCreate,
    IUserUpdate,
)
from app.models.user import User
from app.models.role import Role
from app.schemas.role import IRoleEnum
from app.schemas.common import IOrderEnum
from app.api.v1 import deps
from app.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    UserSelfDeleteException,
    RoleNotFoundException,
)
from app.api.v1.deps import (
    auth,
    bind_repo,
)
from app.db.repositories import (
    UserRepository,
    RoleRepository,
)


router = APIRouter()


@router.get('', response_model=List[IUserRead])
async def get_all_users(
    params: Params = Depends(),
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User)),
    current_user: User = Depends(
        auth.get_current_user(required_roles=[
            IRoleEnum.admin,
            IRoleEnum.manager,
        ])
    )
):
    """
    Retrieve users. Requires admin or manager role
    """
    users = await user_repo.get_multi()
    return users


@router.get("/me", response_model=IUserRead)
async def get_current_user(
    current_user: User = Depends(
        auth.get_current_user()
    )
):
    return current_user


@router.put("/me", response_model=IUserRead)
async def update_current_user(
    request_data: IUserUpdate,
    current_user: User = Depends(
        auth.get_current_user()
    ),
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User))
):
    if request_data.email:
        existed_user: User = await user_repo.get_by_email(
            email=request_data.email
        )
        if existed_user:
            if existed_user.id != current_user.id:
                raise UserAlreadyExistsException()
    updated_user = await user_repo.update_with_role(
        model=current_user,
        data=request_data
    )
    return updated_user


@router.get("/{id}", response_model=IGetResponseBase[IUserRead])
async def get_user_by_id(
    id: int,
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User)),
    current_user: User = Depends(
        auth.get_current_user(required_roles=[
            IRoleEnum.admin,
            IRoleEnum.manager
        ])
    )
):
    """
    Retrieve user by id. Requires admin or manger role
    """
    if user := await user_repo.get(id=id):
        return response(data=user)
    else:
        raise UserNotFoundException()


@router.post(
    "",
    response_model=IUserRead,
    status_code=status.HTTP_201_CREATED
)
async def create_new_user(
    request_data: IUserCreate,
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User)),
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role)),
    current_user: User = Depends(
        auth.get_current_user(required_roles=[
            IRoleEnum.admin
        ])
    ),
):
    """
    Create new user. Requires admin role.
    """
    await auth.user_exists(
        new_user=request_data,
        user_repo=user_repo
    )
    if request_data.role_id:
        role = await role_repo.get(id=request_data.role_id)
        if not role:
            raise RoleNotFoundException()
    new_user = await user_repo.create_with_role(data=request_data)
    return new_user
    # return response(data=new_user)


@router.put("/{id}", response_model=IUserRead)
async def update_user(
    id: int,
    request_data: IUserUpdate,
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User)),
    role_repo: RoleRepository = Depends(bind_repo(RoleRepository, Role)),
    current_user: User = Depends(
        auth.get_current_user(required_roles=[
            IRoleEnum.admin
        ])
    ),
):
    """
    Update existing user.
    """
    user = await auth.is_valid_user(user_id=id, user_repo=user_repo)
    if request_data.email:
        existed_user: User = await user_repo.get_by_email(
            email=request_data.email
        )
        if existed_user:
            if existed_user.id != user.id:
                raise UserAlreadyExistsException()
    if request_data.role_id:
        role = await role_repo.get(id=request_data.role_id)
        if not role:
            raise RoleNotFoundException()
    updated_user = await user_repo.update_with_role(
        model=user,
        data=request_data
    )
    return updated_user
    # return response(data=updated_user)


@router.delete("/{id}", response_model=IUserRead)
async def delete_user(
    id: int,
    user_repo: UserRepository = Depends(bind_repo(UserRepository, User)),
    current_user: User = Depends(deps.auth.get_current_user(required_roles=[
        IRoleEnum.admin
    ]))
):
    await auth.is_valid_user(user_id=id, user_repo=user_repo)
    if current_user.id == id:
        raise UserSelfDeleteException()
    deleted_user = await user_repo.delete(id=id)
    return deleted_user

from fastapi import APIRouter

from app.api.v1.routes import (
    login,
    users,
    roles,
)


api_router = APIRouter()

api_router.include_router(login.router, prefix='/login', tags=['Auth'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(roles.router, prefix='/roles', tags=['Roles'])

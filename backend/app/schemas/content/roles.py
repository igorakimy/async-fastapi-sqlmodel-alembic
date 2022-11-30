from typing import List

from app.schemas.role import IRoleCreate


roles: List[IRoleCreate] = [
    IRoleCreate(name="Админ", slug="admin", description="This the Admin role"),
    IRoleCreate(name="Менеджер", slug="manager", description="Manager role"),
    IRoleCreate(name="Пользователь", slug="user", description="User role"),
]
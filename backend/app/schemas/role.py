from enum import Enum

from app.models.role import RoleBase
from app.utils.partial import optional


class IRoleCreate(RoleBase):
    pass


@optional
class IRoleUpdate(RoleBase):
    pass


class IRoleRead(RoleBase):
    id: int


class IRoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

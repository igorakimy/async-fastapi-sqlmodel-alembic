from enum import Enum
from typing import List

from pydantic import BaseModel

from .role import IRoleRead


class IMetaGeneral(BaseModel):
    roles: List[IRoleRead]


class IOrderEnum(str, Enum):
    ascending = "ascending"
    descending = "descending"


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"

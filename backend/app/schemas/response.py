import math
from typing import (
    Any,
    Dict,
    Generic,
    Sequence,
    Union,
    Optional,
    TypeVar,
    Type,
)

from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage
from pydantic.generics import GenericModel

ResponsePage = TypeVar("ResponsePage", bound="IResponsePage")
DataType = TypeVar("DataType")
T = TypeVar("T")


class PageBase(Page[T], Generic[T]):
    pages: int
    next_page: Optional[int]
    prev_page: Optional[int]

    class Config:
        orm_mode = True


class IResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: Optional[T]


class IResponsePage(AbstractPage[T], Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: PageBase[T]

    __params_type__ = Params

    @classmethod
    def create(
        cls: Type[ResponsePage],
        items: Sequence[T],
        params: Params,
        total: Optional[int] = None
    ) -> Union[PageBase[T], None]:
        pages = math.ceil(total / params.size)
        return cls(data=PageBase(
                items=items,
                page=params.page,
                size=params.size,
                total=total,
                pages=pages,
                next_page=params.page + 1 if params.page < pages else None,
                prev_page=params.page - 1 if params.page > 1 else None,
            ))


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IGetResponsePaginated(IResponsePage[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data created successfully"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated successfully"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted successfully"


def response(
    data: Optional[DataType],
    message: Optional[str] = "",
    meta: Optional[Union[Dict, Any]] = None
) -> Union[Dict[str, DataType], DataType]:
    if meta is None:
        meta = {}
    if isinstance(data, IResponsePage):
        data.message = "Data paginated correctly" if not message else message
        data.meta = meta
        return data
    body_response = {
        "data": data,
        "message": message,
        "meta": meta
    }
    return dict((k, v) for k, v in body_response.items() if v is not None)

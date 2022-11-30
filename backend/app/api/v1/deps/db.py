from typing import (
    Callable,
    AsyncGenerator,
    Type,
    TypeVar
)

from fastapi import HTTPException, Depends
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import async_session
from app.db.repositories.base import BaseRepository


ModelType = TypeVar("ModelType", bound=SQLModel)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = async_session()
    try:
        yield session
    except SQLAlchemyError as exc:
        await session.rollback()
        raise exc
    except HTTPException as exc:
        await session.rollback()
        raise exc
    else:
        await session.commit()
    finally:
        await session.close()


def bind_repo(
    repository: Type[BaseRepository],
    model: Type[ModelType]
) -> Callable:
    def get_repo(
        db: AsyncSession = Depends(get_db)
    ) -> BaseRepository:
        return repository(model, db)
    return get_repo

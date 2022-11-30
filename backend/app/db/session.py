from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

connect_args = {"check_same_thread": False}

engine = create_async_engine(
    settings.ASYNC_DB_URI,
    echo=True,
    future=True,
    pool_size=settings.POOL_SIZE,
    max_overflow=64,
    json_serializer=jsonable_encoder,
)

async_session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)

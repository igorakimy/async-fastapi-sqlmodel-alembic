from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_async_sqlalchemy import db
from fastapi_pagination import add_pagination
from sqlmodel import text

from app.core.config import settings
from app.api.v1.routes import api_router as api_router_v1


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        openapi_url=f"/{settings.API_VERSION}/openapi.json"
    )

    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=settings.ASYNC_DB_URI,
        engine_args={
            "echo": False,
            "pool_pre_ping": True,
            "pool_size": settings.POOL_SIZE,
            "max_overflow": 64,
        },
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/", tags=["Root"])
    async def main():
        return {
            "app_name": settings.PROJECT_NAME,
            "api_version": settings.API_VERSION
        }

    @app.on_event('startup')
    async def startup():
        await add_postgresql_extension()

    @app.on_event('shutdown')
    async def shutdown():
        pass

    app.include_router(api_router_v1, prefix=settings.API_PREFIX)

    add_pagination(app)

    return app


async def add_postgresql_extension() -> None:
    async with db():
        await db.session.execute(
            text('CREATE EXTENSION IF NOT EXISTS pg_trgm')
        )


app = get_application()

import asyncio
import logging
from logging.config import fileConfig

from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine
from alembic import context

from app.core.config import settings
from app.models.role import Role
from app.models.user import User


# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
fileConfig(config.config_file_name)

logger = logging.getLogger('alembic.env')

target_metadata = SQLModel.metadata


config.set_main_option('sqlalchemy.url', settings.ASYNC_DB_URI)


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        create_engine(
            settings.ASYNC_DB_URI,
            echo=True,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    logger.info('Running migrations offline')
    run_migrations_offline()
else:
    logger.info('Running migrations online')
    asyncio.run(run_migrations_online())

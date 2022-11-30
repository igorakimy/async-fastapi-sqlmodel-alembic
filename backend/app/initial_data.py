import asyncio
import logging
from app.db.tasks import exec_all_tasks
from app.db.session import async_session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_init_data() -> None:
    async with async_session():
        await exec_all_tasks()


async def main() -> None:
    logger.info('Executing database tasks...')
    await create_init_data()
    logger.info('All database tasks was executed.')


if __name__ == '__main__':
    asyncio.run(main())

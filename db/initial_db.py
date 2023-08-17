import asyncio

from db.models.models import Base

from .base import engine


async def init_models() -> None:
    """
    Function for deleting old tables from the database
    and creating new ones.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await init_models()


if __name__ == '__main__':
    asyncio.run(main())

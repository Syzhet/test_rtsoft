from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from config.config import base_config

PG_USER: str = base_config.db.db_user
PG_PASS: str = base_config.db.db_password
PG_HOST: str = base_config.db.db_host
PG_PORT: str = base_config.db.db_port
DATABASE: str = base_config.db.database

DATABASE_URL: str = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{DATABASE}"
)

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

async_session: AsyncSession = async_sessionmaker(
    engine, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Function for creating a database connection session."""

    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise error

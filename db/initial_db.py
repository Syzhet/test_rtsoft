import asyncio

from db.models.models import Base

from .base import engine


async def init_models() -> None:
    """
    Функция удаляет старые таблицы и создает их заново.
    """

    # необходимо на первый запуск чтобы контейнер с БД
    # успел инициализироваться
    await asyncio.sleep(5)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    """
    Функция запускает процесс создания
    таблиц в БД PostgreSQL.
    """

    await init_models()


if __name__ == '__main__':
    asyncio.run(main())

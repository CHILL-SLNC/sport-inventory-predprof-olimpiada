from sqlalchemy import text, insert, select, func, cast, Integer, and_
from database import async_engine, async_session_factory
from models import Base, InventoryOrm
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager


# Инициализация класса для создания асинхронных методов на основе ORM.
class AsyncORM:

    # Метод для создания в базе данных всех объявленных таблиц.
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

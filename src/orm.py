from sqlalchemy import text, insert, select, func, cast, Integer, and_
from src.database import async_engine, async_session_factory
from src.models import Base, InventoryOrm
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from src.schemas import InventoryAddDTO, InventoryUpdDTO
from fastapi import APIRouter, HTTPException


# Инициализация класса для создания асинхронных методов на основе ORM.
class AsyncORM:

    # Метод для создания в базе данных всех объявленных таблиц.
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    # Метод для добавления данных об инвентаре.
    @staticmethod
    async def insert_inventory(inventory: InventoryAddDTO):
        async with async_session_factory() as session:
            inv = InventoryOrm(
                name=inventory.name,
                count_new=inventory.count_new,
                count_inuse=inventory.count_inuse,
                count_broken=inventory.count_broken)
            session.add(inv)
            await session.commit()

    # Метод для получения списка инвентаря и информации о нем.
    @staticmethod
    async def select_inventory():
        async with async_session_factory() as session:
            query = select(InventoryOrm)
            result = await session.execute(query)
            inventory = result.scalars().all()
            return inventory

    # Метод для получения информации о конкретном инвентаре.
    @staticmethod
    async def select_inventory_currency(inventory_id: int):
        async with async_session_factory() as session:
            inventory = await session.get(InventoryOrm, inventory_id)
            return inventory

    # Метод для обновления информации о конкретном инвентаре
    @staticmethod
    async def update_inventory(inventory: InventoryUpdDTO):
        async with async_session_factory() as session:
            inventory_cur = await session.get(InventoryOrm, inventory.id)
            if inventory_cur is None:
                raise HTTPException(status_code=404, detail="Инвентарь не найден")
            inventory_cur.count_new = inventory.new_count_new
            inventory_cur.count_broken = inventory.new_count_broken
            inventory_cur.count_inuse = inventory.new_count_inuse
            await session.commit()

    # Метод для удаления информации о конкретном инвентаре.
    @staticmethod
    async def delete_inventory_currency(inventory_id: int):
        async with async_session_factory() as session:
            inventory = await session.get(InventoryOrm, inventory_id)
            if inventory is None:
                raise HTTPException(status_code=404, detail="Инвентарь не найден")
            await session.delete(inventory)
            await session.commit()

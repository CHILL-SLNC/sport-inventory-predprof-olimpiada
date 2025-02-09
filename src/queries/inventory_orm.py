from sqlalchemy import select
from src.database import async_engine, async_session_factory
from src.models import Base, InventoryOrm
from src.schemas.inventory_schemas import InventoryAddDTO, InventoryUpdDTO
from fastapi import HTTPException


# Инициализация класса для создания асинхронных методов на основе ORM.
class AsyncInventoryORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_inventory(inventory_data: InventoryAddDTO):
        async with async_session_factory() as session:
            query = select(InventoryOrm.name)
            names = await session.execute(query)
            if inventory_data.name not in names.scalars().all():
                inventory = InventoryOrm(
                    name=inventory_data.name,
                    count_new=inventory_data.count_new,
                    count_inuse=inventory_data.count_inuse,
                    count_broken=inventory_data.count_broken)
                session.add(inventory)
                await session.commit()
                return {'ok': True, "message": "Инвентарь успешно добавлен"}
            return {'ok': False, "message": "Инвентарь с таким названием уже есть"}

    @staticmethod
    async def select_inventory():
        async with async_session_factory() as session:
            query = select(InventoryOrm)
            result = await session.execute(query)
            inventory = result.scalars().all()
            return inventory

    @staticmethod
    async def select_inventory_currency(inventory_id: int):
        async with async_session_factory() as session:
            inventory = await session.get(InventoryOrm, inventory_id)
            return inventory

    @staticmethod
    async def update_inventory(inventory: InventoryUpdDTO):
        async with async_session_factory() as session:
            query = select(InventoryOrm.name)
            names = await session.execute(query)
            inventory_cur = await session.get(InventoryOrm, inventory.id)
            if inventory_cur is None:
                raise HTTPException(status_code=404, detail="Инвентарь не найден")
            inventory_cur.count_new = inventory.count_new
            inventory_cur.count_broken = inventory.count_broken
            inventory_cur.count_inuse = inventory.count_inuse
            if (inventory.name in names.scalars().all()) and inventory_cur.name != inventory.name:
                raise HTTPException(status_code=409, detail="Инвентарь с таким названием уже есть")
            inventory_cur.name = inventory.name
            await session.commit()

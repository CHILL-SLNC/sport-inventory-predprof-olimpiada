from fastapi import APIRouter, HTTPException
from src.orm import AsyncORM
from src.schemas import InventoryAddDTO, InventoryDTO, InventoryUpdDTO
from src.database import Base, sync_engine
from sqlalchemy import inspect

router = APIRouter()


@router.on_event("startup")
async def startup():
    if sorted(inspect(sync_engine).get_table_names()) != sorted(list(Base.metadata.tables.keys())):
        await AsyncORM.create_tables()
        print(inspect(sync_engine).get_table_names())
        print(list(Base.metadata.tables.keys()))


# Эндпоинт для добавления данных об инвентаре.
@router.post("/inventory_add", tags=["Инвентарь"],
             summary="Добавить новый инвентарь")
async def create_newInventory(inventory: InventoryAddDTO):
    result = await AsyncORM.insert_inventory(inventory)
    return {'ok': True, "message": "Инвентарь успешно добавлен"}


# Эндпоинт для получения списка инвентаря и информации о нем.
@router.get("/inventory_get", tags=["Инвентарь"],
            summary="Получить весь список инвентаря")
async def get_inventoryList() -> list[InventoryDTO]:
    result = await AsyncORM.select_inventory()
    return result


# Эндпоинт для получения информации о конкретном инвентаре.
@router.get("/inventory_get/{inventory_id}", tags=["Инвентарь"],
            summary="Получить информацию о конкретном инвентаре")
async def get_inventoryCurency(inventory_id: int) -> InventoryDTO:
    result = await AsyncORM.select_inventory_currency(inventory_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Инвентарь не найден")
    return result


# Эндпоинт для обновления информации о конкретном инвентаре
@router.put("/inventory_update/{inventory_inf}", tags=["Инвентарь"],
            summary="Изменить информацию об инвентаре")
async def update_inventoryCurrency(inventory: InventoryUpdDTO):
    result = await AsyncORM.update_inventory(inventory)
    return {'ok': True, "message": "Информация об инвентаре успешно обновлена"}


# Эндпоинт для удаления информации о конкретном инвентаре.
@router.delete("/inventory_delete/{inventory_id}", tags=["Инвентарь"],
               summary="Удалить информацию о конкретном инвентаре")
async def delete_inventoryCurency(inventory_id: int):
    result = await AsyncORM.delete_inventory_currency(inventory_id)
    return {'ok': True, "message": "Информация об инвентаре успешно удалена"}

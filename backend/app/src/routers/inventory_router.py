from fastapi import APIRouter, HTTPException
from src.queries.inventory_orm import AsyncInventoryORM
from src.queries.admin_orm import AsyncAdminORM
from src.schemas.inventory_schemas import InventoryAddDTO, InventoryDTO, InventoryUpdDTO
from src.database import Base, sync_engine
from sqlalchemy import inspect

router = APIRouter()



@router.on_event("startup")
async def startup():
    if sorted(inspect(sync_engine).get_table_names()) != sorted(list(Base.metadata.tables.keys())):
        await AsyncInventoryORM.create_tables()
        await AsyncAdminORM.set_admin()
        print(inspect(sync_engine).get_table_names())
        print(list(Base.metadata.tables.keys()))


@router.post("/inventory_add", tags=["Инвентарь"],
             summary="Добавить новый инвентарь")
async def create_newInventory(inventory_data: InventoryAddDTO):
    result = await AsyncInventoryORM.insert_inventory(inventory_data)
    if not result['ok']:
        raise HTTPException(status_code=409, detail=result["message"])
    return result


@router.get("/inventory_get", tags=["Инвентарь"],
            summary="Получить весь список инвентаря")
async def get_inventoryList() -> list[InventoryDTO]:
    result = await AsyncInventoryORM.select_inventory()
    return result


@router.get("/inventory_get/{inventory_id}", tags=["Инвентарь"],
            summary="Получить информацию о конкретном инвентаре")
async def get_inventoryCurency(inventory_id: int) -> InventoryDTO:
    result = await AsyncInventoryORM.select_inventory_currency(inventory_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Инвентарь не найден")
    return result


@router.put("/inventory_update", tags=["Инвентарь"],
            summary="Изменить информацию об инвентаре")
async def update_inventoryCurrency(inventory_data: InventoryUpdDTO):
    result = await AsyncInventoryORM.update_inventory(inventory_data)
    return {'ok': True, "message": "Информация об инвентаре успешно обновлена"}


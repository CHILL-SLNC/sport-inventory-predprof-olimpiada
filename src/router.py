from fastapi import APIRouter, HTTPException, Depends, Request, Response
from authx import AuthX, AuthXConfig
from src.orm import AsyncInventoryORM, AsyncUserORM
from src.schemas import InventoryAddDTO, InventoryDTO, InventoryUpdDTO, UsersAddDTO, UsersLoginDTO, UsersUpdDTO, \
    UsersDTO, ApplicationsAddDTO
from src.database import Base, sync_engine
from sqlalchemy import inspect
import jwt
import json

router = APIRouter()

auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = 'SECRET_KEY'
auth_config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
auth_config.JWT_TOKEN_LOCATION = ["cookies"]
auth_config.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=auth_config)


# Добавление таблиц в базу данных при необходимости.
@router.on_event("startup")
async def startup():
    if sorted(inspect(sync_engine).get_table_names()) != sorted(list(Base.metadata.tables.keys())):
        await AsyncInventoryORM.create_tables()
        print(inspect(sync_engine).get_table_names())
        print(list(Base.metadata.tables.keys()))


# Эндпоинт для добавления данных об инвентаре.
@router.post("/inventory_add/{inventory_data}", tags=["Инвентарь"],
             summary="Добавить новый инвентарь")
async def create_newInventory(inventory_data: InventoryAddDTO):
    result = await AsyncInventoryORM.insert_inventory(inventory_data)
    if not result['ok']:
        raise HTTPException(status_code=409, detail=result["message"])
    return result


# Эндпоинт для получения списка инвентаря и информации о нем.
@router.get("/inventory_get", tags=["Инвентарь"],
            summary="Получить весь список инвентаря")
async def get_inventoryList() -> list[InventoryDTO]:
    result = await AsyncInventoryORM.select_inventory()
    return result


# Эндпоинт для получения информации о конкретном инвентаре.
@router.get("/inventory_get/{inventory_id}", tags=["Инвентарь"],
            summary="Получить информацию о конкретном инвентаре")
async def get_inventoryCurency(inventory_id: int) -> InventoryDTO:
    result = await AsyncInventoryORM.select_inventory_currency(inventory_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Инвентарь не найден")
    return result


# Эндпоинт для обновления информации о конкретном инвентаре
@router.put("/inventory_update/{inventory_data}", tags=["Инвентарь"],
            summary="Изменить информацию об инвентаре")
async def update_inventoryCurrency(inventory_data: InventoryUpdDTO):
    result = await AsyncInventoryORM.update_inventory(inventory_data)
    return {'ok': True, "message": "Информация об инвентаре успешно обновлена"}


# Эндпоинт для удаления информации о конкретном инвентаре.
@router.delete("/inventory_delete/{inventory_id}", tags=["Инвентарь"],
               summary="Удалить информацию о конкретном инвентаре")
async def delete_inventoryCurency(inventory_id: int):
    result = await AsyncInventoryORM.delete_inventory_currency(inventory_id)
    return {'ok': True, "message": "Информация об инвентаре успешно удалена"}


# Эндпоинт для добавления данных о пользователе.
@router.post("/user_add/{user_data}", tags=["Пользователь"],
             summary="Добавить нового пользователя")
async def create_newUser(user_data: UsersAddDTO):
    result = await AsyncUserORM.insert_user(user_data)
    if not result['ok']:
        raise HTTPException(status_code=409, detail=result["message"])
    return result


# Эндпоинт для авторизации пользователя.
@router.post("/user_login/{user_auth}", tags=["Пользователь"],
             summary='Авторизовать пользователя')
async def login_user(cred: UsersLoginDTO, response: Response):
    result = await AsyncUserORM.login_user(cred)
    if result is None:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    token = security.create_access_token(uid=result, data={"role": "user"})
    response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)


# Эндпоинт для получения роли пользователя.
@router.get("/role_get", tags=["Пользователь", "Админ"],
            summary='Получить роль пользователя', dependencies=[Depends(security.access_token_required)])
async def get_role(request: Request) -> str:
    token = security._decode_token((await security.get_access_token_from_request(request)).token)
    role = json.loads(token.model_dump_json()).get("role")
    return role


# Эндпоинт для получения логина пользователя.
@router.get("/login_get", tags=["Пользователь", "Админ"],
            summary='Получить логин', dependencies=[Depends(security.access_token_required)])
async def get_login(request: Request) -> str:
    token = security._decode_token((await security.get_access_token_from_request(request)).token)
    login = json.loads(token.model_dump_json()).get("sub")
    return login


# Эндпоинт для получения информации о конкретном пользователе.
@router.get("/user_get", tags=["Пользователь"],
            summary="Получить информацию о конкретном пользователе",
            dependencies=[Depends(security.access_token_required)])
async def get_user(request: Request) -> UsersDTO:
    login = await get_login(request)
    result = await AsyncUserORM.get_user(login)
    return result


# Эндпоинт для изменения информации о пользователе.
@router.put("/user_update/{new_user_data}", tags=["Пользователь"],
            summary='Изменить информацию о пользователе', dependencies=[Depends(security.access_token_required)])
async def update_user(user_data: UsersUpdDTO, request: Request):
    login = await get_login(request)
    await AsyncUserORM.update_user(user_data, login)
    return {"ok": True, "message": f"Информация о пользователе {login} успешно изменена"}


# Эндпоинт для смены пароля пользователя.
@router.put("/user_password_update/{new_password}", tags=["Пользователь"],
            summary='Изменить пароль пользователя', dependencies=[Depends(security.access_token_required)])
async def update_passsword_user(new_password: str, request: Request):
    login = await get_login(request)
    await AsyncUserORM.update_password_user(new_password, login)
    return {"ok": True, "message": f"Пароль пользователя {login} успешно изменен"}


# Эндпоинт для создания заявки на использования инвентаря.
@router.post("/application_create/{application_data}", tags=["Пользователь"],
             summary="Создать заявку")
async def create_application(appl_data: ApplicationsAddDTO, request: Request):
    login = await get_login(request)
    result = await AsyncUserORM.insert_application(appl_data, login)
    return result

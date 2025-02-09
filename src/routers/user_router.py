from fastapi import APIRouter, HTTPException, Header
from src.queries.user_orm import AsyncUserORM
from src.schemas.user_schemas import UsersAddDTO, UsersDTO
from src.schemas.appl_schemas import ApplicationsDTO, ApplicationsAddDTO
from src.auth import Auth

router = APIRouter()



@router.post("/user_add", tags=["Пользователь"],
             summary="Добавить нового пользователя")
async def create_newUser(user_data: UsersAddDTO):
    result = await AsyncUserORM.insert_user(user_data)
    if not result['ok']:
        raise HTTPException(status_code=409, detail=result["message"])
    return result



@router.get("/user_get", tags=["Пользователь"],
            summary="Получить информацию о конкретном пользователе", )
async def get_user(authorization: str = Header(...)) -> UsersDTO:
    username = await Auth.get_username(authorization)
    result = await AsyncUserORM.get_user(username)
    return result


@router.post("/application_create", tags=["Пользователь"],
             summary="Создать заявку")
async def create_application(appl_data: ApplicationsAddDTO, authorization: str = Header(...)):
    username = await Auth.get_username(authorization)
    result = await AsyncUserORM.insert_application(appl_data, username)
    return result


@router.get("/applications_user_get", tags=["Пользователь"],
            summary="Получить заявки пользователя")
async def get_user_applications(authorization: str = Header(...)) -> list[ApplicationsDTO] | None:
    username = await Auth.get_username(authorization)
    applications = await AsyncUserORM.get_user_applications(username)
    return applications


@router.put('/application_close/{appl_id}', tags=["Пользователь"],
            summary="Закрыть заявку на использования инвентаря")
async def close_application(appl_id: int):
    result = await AsyncUserORM.close_application(appl_id)
    return {"ok": True, "message": f"Заявка {appl_id} закрыта"}

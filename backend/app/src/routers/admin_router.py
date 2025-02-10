from fastapi import APIRouter, Header
from src.queries.admin_orm import AsyncAdminORM
from src.schemas.admin_schemas import AdminsDTO
from src.schemas.plans_schemas import PurchPlansDTO, PurchPlansAddDTO
from src.schemas.appl_schemas import ApplicationsDTO, ApplicationsCommentDTO
from src.auth import Auth

router = APIRouter()


@router.get("/admin_get", tags=["Администратор"], summary="Получить информацию о конкретном администраторе")
async def get_admin(authorization: str = Header(...)) -> AdminsDTO:
    username = await Auth.get_username(authorization)
    result = await AsyncAdminORM.get_admin(username)
    return result


@router.get("/applications_get", tags=["Администратор"],
            summary="Получить весь список заявок")
async def get_applications() -> list[ApplicationsDTO] | None:
    result = await AsyncAdminORM.get_applications()
    return result


@router.put('/application_approve/{appl_id}', tags=["Администратор"],
            summary="Принять заявку на использования инвентаря")
async def approve_application(appl_id: int):
    result = await AsyncAdminORM.approve_application(appl_id)
    return {"ok": True, "message": f"Заявка {appl_id} была принята"}


@router.put('/application_reject/{appl_id}', tags=["Администратор"],
            summary="Отклонить заявку на использования инвентаря")
async def reject_application(appl_id: int):
    result = await AsyncAdminORM.reject_application(appl_id)
    return {"ok": True, "message": f"Заявка {appl_id} была отклонена"}


@router.post('/plan_add', tags=["Администратор"],
             summary="Добавить план закупки")
async def plan_add(plan_data: PurchPlansAddDTO, authorization: str = Header(...)):
    username = await Auth.get_username(authorization)
    result = await AsyncAdminORM.insert_purch_plan(plan_data, username)
    return {"ok": True, "message": f"План закупки успешно создан"}


@router.post('/plan_activate/{plan_id}', tags=["Администратор"],
             summary="Активировать план закупки")
async def plan_activate(plan_id: int, authorization: str = Header(...)):
    username = await Auth.get_username(authorization)
    result = await AsyncAdminORM.activate_purch_plan(plan_id, username)
    return {"ok": True, "message": f"План закупки успешно активирован"}


@router.get("/purchase_plans_get", tags=["Администратор"],
            summary="Получить весь список планов закупок")
async def get_plans(authorization: str = Header(...)) -> list[PurchPlansDTO]:
    username = await Auth.get_username(authorization)
    result = await AsyncAdminORM.get_purchases(username)
    return result


@router.post("/application_comment", tags=["Администратор"],
             summary="Добавить комментарий к заявке")
async def add_comment(comment_data: ApplicationsCommentDTO):
    result = await AsyncAdminORM.add_comment(comment_data.application_id, comment_data.comment)
    return {"ok": True, "message": f"Комментарий успешно добавлен"}


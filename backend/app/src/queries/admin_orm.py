from sqlalchemy import select
from src.database import async_session_factory
from src.models import InventoryOrm, ApplicationsOrm, AdminsOrm, PurchasePlanOrm, ApplStatus
from sqlalchemy.orm import selectinload
from src.schemas.admin_schemas import AdminsDTO
from src.schemas.appl_schemas import ApplicationsDTO
from src.schemas.plans_schemas import PurchPlansAddDTO, PurchPlansDTO
from src.config import settings
from src.auth import Auth
from fastapi import HTTPException


class AsyncAdminORM:
    @staticmethod
    async def set_admin():
        async with async_session_factory() as session:
            inventory = AdminsOrm(
                username=settings.ADMIN_USERNAME,
                hashed_password=await Auth.get_password_hash(settings.ADMIN_PASSWORD),
                firstname=settings.ADMIN_FIRST_NAME,
                lastname=settings.ADMIN_LASTNAME,
                second_lastname=settings.ADMIN_SECOND_LASTNAME
            )
            session.add(inventory)
            await session.commit()
            return {'ok': True, "message": "Админ успешно добавлен"}

    @staticmethod
    async def get_admin(username: str) -> AdminsDTO:
        async with async_session_factory() as session:
            query = (
                select(AdminsOrm)
                .filter(AdminsOrm.username == username)
                .options(selectinload(AdminsOrm.purch_plans))
            )
            result = await session.execute(query)
            admin = result.scalars().first()
            return AdminsDTO.from_orm(admin)

    @staticmethod
    async def get_password(username: str) -> str:
        async with async_session_factory() as session:
            query = (
                select(AdminsOrm)
                .filter(AdminsOrm.username == username)
                .options(selectinload(AdminsOrm.purch_plans))
            )
            result = await session.execute(query)
            admin = result.scalars().first()
            if admin is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            return admin.hashed_password

    @staticmethod
    async def get_applications() -> list[ApplicationsDTO]:
        async with async_session_factory() as session:
            query = select(ApplicationsOrm)
            result = await session.execute(query)
            applications = result.scalars().all()
            return [ApplicationsDTO.from_orm(application) for application in applications]

    @staticmethod
    async def approve_application(appl_id: int):
        async with async_session_factory() as session:
            appl = await session.get(ApplicationsOrm, appl_id)
            if appl.status != ApplStatus.undConsid:
                raise HTTPException(status_code=409, detail='Заявка не находится на рассмотрении.')
            appl.status = "approved"
            inventory = await session.get(InventoryOrm, appl.inventory_id)
            inventory.count_new -= appl.count
            inventory.count_inuse += appl.count
            await session.commit()

    @staticmethod
    async def reject_application(appl_id):
        async with async_session_factory() as session:
            appl = await session.get(ApplicationsOrm, appl_id)
            if appl.status != ApplStatus.undConsid:
                raise HTTPException(status_code=409, detail='Заявка не находится на рассмотрении.')
            appl.status = "denied"
            await session.commit()

    @staticmethod
    async def insert_purch_plan(plan_data: PurchPlansAddDTO, username: str):
        async with async_session_factory() as session:
            inventory = await session.get(InventoryOrm, plan_data.inventory_id)
            if inventory is None:
                raise HTTPException(status_code=404, detail="Инвентарь не найден")
            plan = PurchasePlanOrm(
                admin_id=username,
                inventory_id=plan_data.inventory_id,
                inventory_name=inventory.name,
                count=plan_data.count,
                cost=plan_data.cost,
                provider=plan_data.provider
            )
            session.add(plan)
            await session.commit()
            return {'ok': True, "message": "План успешно добавлен"}

    @staticmethod
    async def activate_purch_plan(plan_id: int, username: str):
        async with async_session_factory() as session:
            plan = await session.get(PurchasePlanOrm, plan_id)
            if plan == None:
                raise HTTPException(status_code=404, detail="План закупки не найден")
            elif plan.admin_id != username:
                raise HTTPException(status_code=403, detail='Вы пытаетесь активировать план другого администратора.')
            inventory = await session.get(InventoryOrm, plan.inventory_id)
            inventory.count_new += plan.count
            await session.delete(plan)
            await session.commit()

    @staticmethod
    async def get_purchases(admin_id) -> list[PurchPlansDTO]:
        async with async_session_factory() as session:
            query = (select(PurchasePlanOrm)
                     .filter(PurchasePlanOrm.admin_id == admin_id))
            result = await session.execute(query)
            plans = result.scalars().all()
            return [PurchPlansDTO.from_orm(plan) for plan in plans]

    @staticmethod
    async def add_comment(appl_id: int, comment: str):
        async with async_session_factory() as session:
            appl = await session.get(ApplicationsOrm, appl_id)
            if appl.status != ApplStatus.closed:
                raise HTTPException(status_code=409, detail='Заявка не закрыта.')
            appl.comment = comment
            print(appl.comment)
            print(comment)
            await session.commit()

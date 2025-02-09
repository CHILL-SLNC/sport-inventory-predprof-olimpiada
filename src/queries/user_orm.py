from sqlalchemy import select
from src.database import async_session_factory
from src.models import InventoryOrm, UsersOrm, ApplicationsOrm, ApplStatus
from sqlalchemy.orm import selectinload
from src.schemas.user_schemas import UsersAddDTO, UsersUpdDTO, UsersDTO
from src.schemas.appl_schemas import ApplicationsDTO, ApplicationsAddDTO
from fastapi import HTTPException
from src.auth import Auth
import datetime


class AsyncUserORM:
    # Метод для добавления данных о пользователе.
    @staticmethod
    async def insert_user(user_data: UsersAddDTO):
        async with async_session_factory() as session:
            query = select(UsersOrm.username)
            usernames = await session.execute(query)
            password = await Auth.get_password_hash(user_data.password)
            if user_data.username not in usernames.scalars().all():
                user = UsersOrm(
                    username=user_data.username,
                    firstname=user_data.firstname,
                    lastname=user_data.lastname,
                    second_lastname=user_data.second_lastname,
                    hashed_password=password)
                session.add(user)
                await session.commit()
                return {'ok': True, "message": "Пользователь успешно добавлен"}
            return {'ok': False, "message": "Пользователь с таким логином уже есть"}

    # Метод для обновления данных о пользователе.
    @staticmethod
    async def update_user(user_data: UsersUpdDTO, login: str):
        async with async_session_factory() as session:
            user = await session.get(UsersOrm, login)
            user.firstname = user_data.firstname
            user.lastname = user_data.lastname
            user.second_lastname = user_data.second_lastname
            await session.commit()

    # Метод для получения данных о пользователе.
    @staticmethod
    async def get_user(username: str) -> UsersDTO | HTTPException:
        async with async_session_factory() as session:
            query = (
                select(UsersOrm)
                .filter(UsersOrm.username == username)
                .options(selectinload(UsersOrm.applications))
            )
            result = await session.execute(query)
            user = result.scalars().first()
            if user is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            return UsersDTO.from_orm(user)

    # Метод для получения данных о пользователе.
    @staticmethod
    async def get_password(username: str) -> str | HTTPException:
        async with async_session_factory() as session:
            query = (
                select(UsersOrm)
                .filter(UsersOrm.username == username)
                .options(selectinload(UsersOrm.applications))
            )
            result = await session.execute(query)
            user = result.scalars().first()
            if user is None:
                raise HTTPException(status_code=404, detail="Пользователь не найден")
            return user.hashed_password

    # Метод для добавления данных о заявке.
    @staticmethod
    async def insert_application(apl_data: ApplicationsAddDTO, username: str):
        async with async_session_factory() as session:
            inventory = await session.get(InventoryOrm, apl_data.inventory_id)
            if inventory is None:
                raise HTTPException(status_code=404, detail="Инвентарь не найден")
            if inventory.count_new < apl_data.count:
                raise HTTPException(status_code=409, detail='Такое количество инвентаря недоступно')
            application = ApplicationsOrm(
                user_id=username,
                created_at=datetime.datetime.utcnow(),
                status='undConsid',
                inventory_id=apl_data.inventory_id,
                inventory_name=inventory.name,
                count=apl_data.count,
                comment=None
            )
            session.add(application)
            await session.commit()
            return {'ok': True, "message": "Заявка успешно добавлена"}
    #
    @staticmethod
    async def get_user_applications(login: str) -> list[ApplicationsDTO]:
        async with async_session_factory() as session:
            query = (select(ApplicationsOrm)
                     .filter(ApplicationsOrm.user_id == login))
            result = await session.execute(query)
            applications = result.scalars().all()
            return applications

    # Метод для закрытия заявки.
    @staticmethod
    async def close_application(appl_id: int):
        async with async_session_factory() as session:
            appl = await session.get(ApplicationsOrm, appl_id)
            if appl.status == ApplStatus.closed:
                raise HTTPException(status_code=409, detail='Заявка уже закрыта.')
            elif appl.status != ApplStatus.approved:
                print(appl.status)
                raise HTTPException(status_code=409, detail='Заявка не была принята.')
            inventory = await session.get(InventoryOrm, appl.inventory_id)
            inventory.count_new += appl.count
            inventory.count_inuse -= appl.count
            appl.status = "closed"
            appl.closed_at = datetime.datetime.utcnow()
            await session.commit()

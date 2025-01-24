from sqlalchemy import text, insert, select, func, cast, Integer, and_
from src.database import async_engine, async_session_factory
from src.models import Base, InventoryOrm, UsersOrm, ApplicationsOrm, AdminsOrm, PurchasePlanOrm
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from src.schemas import InventoryAddDTO, InventoryUpdDTO, UsersAddDTO, UsersLoginDTO, UsersUpdDTO, ApplicationsAddDTO, \
    UsersDTO
from fastapi import APIRouter, HTTPException, Response
import datetime


# Инициализация класса для создания асинхронных методов на основе ORM.
class AsyncInventoryORM:

    # Метод для создания в базе данных всех объявленных таблиц.
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    # Метод для добавления данных об инвентаре.
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


class AsyncUserORM:
    # Метод для добавления данных о пользователе.
    @staticmethod
    async def insert_user(user_data: UsersAddDTO):
        async with async_session_factory() as session:
            query = select(UsersOrm.login)
            logins = await session.execute(query)
            if user_data.login not in logins.scalars().all():
                user = UsersOrm(
                    login=user_data.login,
                    firstname=user_data.firstname,
                    lastname=user_data.lastname,
                    password=user_data.password, )
                session.add(user)
                await session.commit()
                return {'ok': True, "message": "Пользователь успешно добавлен"}
            return {'ok': False, "message": "Пользователь с таким логином уже есть"}

    # Метод для авторизации пользователя.
    @staticmethod
    async def login_user(cred: UsersLoginDTO):
        async with async_session_factory() as session:
            query = select(UsersOrm.password, UsersOrm.login)
            result = await session.execute(query)
            users = {user.login: user.password for user in result.fetchall()}
            if cred.login in users.keys():
                if users[cred.login] == cred.password:
                    return cred.login
            return None

    # Метод для обновления данных о пользователе.
    @staticmethod
    async def update_user(user_data: UsersUpdDTO, login: str):
        async with async_session_factory() as session:
            user = await session.get(UsersOrm, login)
            user.firstname = user_data.firstname
            user.lastname = user_data.lastname
            await session.commit()

    # Метод для получения данных о пользователе.
    @staticmethod
    async def get_user(login: str):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm)
                .filter(UsersOrm.login==login)
                .options(selectinload(UsersOrm.applications))
            )
            result = await session.execute(query)
            user = result.scalars().first()
            return UsersDTO.from_orm(user)

    # Метод для смене пароля пользователя.
    @staticmethod
    async def update_password_user(new_password: str, login: str):
        async with async_session_factory() as session:
            user = await session.get(UsersOrm, login)
            user.password = new_password
            await session.commit()

    # Метод для добавления данных о заявке.
    @staticmethod
    async def insert_application(apl_data: ApplicationsAddDTO, login: str):
        async with async_session_factory() as session:
            inventory = await session.get(InventoryOrm, apl_data.inventory_id)
            if inventory is None:
                raise HTTPException(status_code=404, detail="Инвентарь не найден")
            if inventory.count_new < apl_data.count:
                raise HTTPException(status_code=409, detail='Такое количество инвентаря недоступно')
            application = ApplicationsOrm(
                user_id=login,
                created_at=datetime.datetime.utcnow(),
                status='undConsid',
                inventory_id=apl_data.inventory_id,
                inventory_name=inventory.name,
                count=apl_data.count,
                comment=apl_data.comment,
            )
            session.add(application)
            await session.commit()
            return {'ok': True, "message": "Заявка успешно добавлена"}


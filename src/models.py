from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, Enum, DateTime, \
    CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, str_256, str_512
from typing import Annotated
import enum
import datetime

# Класс для первичного ключа-id.
intpk = Annotated[int, mapped_column(primary_key=True)]

# Класс для первичного ключа-username.
usernamepk = Annotated[str, mapped_column(String(50), primary_key=True)]

# Классы для временных меток в классе ApplicationsOrm.
created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow(), )]
closed_at = Annotated[datetime.datetime, mapped_column(default=None,)]


# Enum-класс для статуса заявок на использование инвентаря.
class ApplStatus(enum.Enum):
    undConsid = 'На рассмотрении'
    denied = 'Отклонена'
    approved = 'Одобрена'
    closed = 'Завершена'


# Объявляем таблицу инвентаря.
class InventoryOrm(Base):
    __tablename__ = 'inventory'
    id: Mapped[intpk]
    name: Mapped[str_256]
    count_new: Mapped[int | None]
    count_broken: Mapped[int | None]
    count_inuse: Mapped[int | None]


# Объявляем таблицу админов.
class AdminsOrm(Base):
    __tablename__ = 'admins'
    login: Mapped[usernamepk]
    password: Mapped[str_256]
    firstname: Mapped[str_256]
    lastname: Mapped[str_256]
    purchPlans: Mapped[list["PurchasePlanOrm"]] = relationship(
        back_populates="admin"
    )


# Объявляем таблицу пользователей.
class UsersOrm(Base):
    __tablename__ = 'users'
    login: Mapped[usernamepk]
    password: Mapped[str_256]
    firstname: Mapped[str_256]
    lastname: Mapped[str_256]
    applications: Mapped[list["ApplicationsOrm"]] = relationship(
        back_populates='user'
    )


# Объявляем таблицу заявок на инвентарь.
class ApplicationsOrm(Base):
    __tablename__ = 'applications'
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.login', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    closed_at: Mapped[closed_at | None]
    status: Mapped[ApplStatus]
    inventory_id: Mapped[int]
    inventory_name: Mapped[str_256]
    count: Mapped[int]
    comment: Mapped[str_256]

    user: Mapped["UsersOrm"] = relationship(
        back_populates='applications',
    )


# Объявляем таблицу планов покупок.
class PurchasePlanOrm(Base):
    __tablename__ = 'purch_plan'
    id: Mapped[intpk]
    admin_id: Mapped[int] = mapped_column(ForeignKey('admins.id', ondelete='CASCADE'))
    inventoryName: Mapped[str_256]
    count: Mapped[int]
    cost: Mapped[int]
    provider: Mapped[str_256]
    admin: Mapped["AdminsOrm"] = relationship(
        back_populates='purchPlans'
    )

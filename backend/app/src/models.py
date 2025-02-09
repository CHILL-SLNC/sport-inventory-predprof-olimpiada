from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, str_256
from typing import Annotated
import enum
import datetime

# Класс для первичного ключа-id.
intpk = Annotated[int, mapped_column(primary_key=True)]

# Класс для первичного ключа-username.
usernamepk = Annotated[str, mapped_column(String(50), primary_key=True)]

# Классы для временных меток в классе ApplicationsOrm.
created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow(), )]
closed_at = Annotated[datetime.datetime, mapped_column(default=None, )]


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
    username: Mapped[usernamepk]
    hashed_password: Mapped[str_256]
    firstname: Mapped[str_256]
    lastname: Mapped[str_256]
    second_lastname: Mapped[str_256]
    purch_plans: Mapped[list["PurchasePlanOrm"]] = relationship(
        back_populates="admin", cascade="save-update, merge"
    )


# Объявляем таблицу пользователей.
class UsersOrm(Base):
    __tablename__ = 'users'
    username: Mapped[usernamepk]
    hashed_password: Mapped[str_256]
    firstname: Mapped[str_256]
    lastname: Mapped[str_256]
    second_lastname: Mapped[str_256]
    applications: Mapped[list["ApplicationsOrm"]] = relationship(
        back_populates='user'
    )


# Объявляем таблицу заявок на инвентарь.
class ApplicationsOrm(Base):
    __tablename__ = 'applications'
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.username', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    closed_at: Mapped[closed_at | None]
    status: Mapped[ApplStatus]
    inventory_id: Mapped[int]
    inventory_name: Mapped[str_256]
    count: Mapped[int]
    comment: Mapped[str_256 | None]

    user: Mapped["UsersOrm"] = relationship(
        back_populates='applications',
    )


# Объявляем таблицу планов покупок.
class PurchasePlanOrm(Base):
    __tablename__ = 'purch_plan'
    id: Mapped[intpk]
    admin_id: Mapped[int] = mapped_column(ForeignKey('admins.username', ondelete='CASCADE'))
    inventory_id: Mapped[int]
    inventory_name: Mapped[str_256]
    count: Mapped[int]
    cost: Mapped[int]
    provider: Mapped[str_256]
    admin: Mapped["AdminsOrm"] = relationship(
        back_populates='purch_plans'
    )

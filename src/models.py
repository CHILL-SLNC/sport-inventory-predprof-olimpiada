from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, Enum, DateTime, \
    CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256, str_512
from typing import Annotated
import enum
import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow(), )]
closed_at = Annotated[datetime.datetime, mapped_column(
    default=datetime.datetime.utcnow(),
    onupdate=datetime.datetime.utcnow(),
)]


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
    id: Mapped[intpk]
    username: Mapped[str_256]
    password: Mapped[str_256]
    purchPlans: Mapped[list["PurchasePlanOrm"]] = relationship(
        back_populates= "admin"
    )

class UsersOrm(Base):
    __tablename__ = 'users'
    id: Mapped[intpk]
    username: Mapped[str_256]
    password: Mapped[str_256]
    applications: Mapped[list["ApplicationsOrm"]] = relationship(
        back_populates='user'
    )


class ApplicationsOrm(Base):
    __tablename__ = 'applications'
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[created_at]
    closed_at: Mapped[closed_at]
    status: Mapped[ApplStatus]
    inventoryName: Mapped[str_256]
    count: Mapped[int]
    comment: Mapped[str_256]

    user: Mapped["UsersOrm"] = relationship(
        back_populates='applications',
    )

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
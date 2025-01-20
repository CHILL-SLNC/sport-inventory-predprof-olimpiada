from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, Enum, DateTime, \
    CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
from typing import Annotated
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]


# Объявляем таблицу инвентаря.
class InventoryOrm(Base):
    __tablename__ = 'inventory'
    id: Mapped[intpk]
    name: Mapped[str_256]
    count_new: Mapped[int | None]
    count_broken: Mapped[int | None]
    count_inuse: Mapped[int | None]

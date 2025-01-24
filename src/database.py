from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String
from src.config import settings
from typing import Annotated

# Инициализация асинхронного движка.
async_engine = create_async_engine(
    url=settings.DATABASE_URL_aiomysql,
    echo=True
)

# Инициализация синхронного движка.
sync_engine = create_engine(
    url=settings.DATABASE_URL_pymysql,
    echo=True
)

# Инициализация фабрики сессий.
async_session_factory = async_sessionmaker(async_engine)

# Введения типа данных "строка до 256 символов в длину".
str_256 = Annotated[str, 256]
str_512 = Annotated[str, 512]


# Инициализации класса базы данных.
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

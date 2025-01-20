from fastapi import FastAPI
from orm import AsyncORM
from asyncio import run
from database import Base, sync_engine
from sqlalchemy import inspect

if inspect(sync_engine).get_table_names()!=list(Base.metadata.tables.keys()):
    run(AsyncORM.create_tables())



from datetime import datetime
from typing import Optional
import src.models
from src.database import str_256
from pydantic import BaseModel, ConfigDict
from src.models import ApplicationsOrm, ApplStatus
import datetime


# Класс для валидации данных об инвентаре при их добавлении.
class InventoryAddDTO(BaseModel):
    name: str
    count_new: Optional[int]
    count_broken: Optional[int]
    count_inuse: Optional[int]


# Класс для валидации данных об инвентаре  при их отображении.
class InventoryDTO(InventoryAddDTO):
    id: int


# Класс для валидации данных об инвентаре  при их обновлении.
class InventoryUpdDTO(BaseModel):
    id: int
    new_count_new: Optional[int]
    new_count_broken: Optional[int]
    new_count_inuse: Optional[int]

# Класс для валидации данных о пользователе при его авторизации.
class UsersLoginDTO(BaseModel):
    login: str
    password: str

# Класс для валидации данных о пользователе при его регистрации.
class UsersAddDTO(UsersLoginDTO):
    firstname: str
    lastname: str

# Класс для валидации данных о пользователе при его обновлении.
class UsersUpdDTO(BaseModel):
    firstname: str
    lastname: str

# Класс для валидации данных о заявках при их добавлении.
class ApplicationsAddDTO(BaseModel):
    inventory_id: int
    count: int
    comment: str

# Класс для валидации данных о заявках при их отображении.
class ApplicationsDTO(ApplicationsAddDTO):
    id: int
    user_id: str
    created_at: datetime.datetime
    closed_at: datetime.datetime | None
    status: ApplStatus
    inventory_name: str

    class Config:
        orm_mode = True
        from_attributes = True

# Класс для валидации данных о пользователе при его отображении.
class UsersDTO(BaseModel):
    login: str
    firstname: str
    lastname: str
    applications: list[ApplicationsDTO]

    class Config:
        orm_mode = True
        from_attributes = True
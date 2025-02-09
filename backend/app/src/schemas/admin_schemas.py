from pydantic import BaseModel
from src.schemas.plans_schemas import PurchPlansDTO


# Класс для валидации данных об администраторе при их отображении.
class AdminsDTO(BaseModel):
    username: str
    firstname: str
    lastname: str
    second_lastname: str
    purch_plans: list[PurchPlansDTO]

    class Config:
        orm_mode = True
        from_attributes = True


# Класс для валидации данных об администраторе при его обновлении.
class AdminsUpdDTO(BaseModel):
    firstname: str
    lastname: str
    second_lastname: str


class AdminsAddDTO(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    second_lastname: str

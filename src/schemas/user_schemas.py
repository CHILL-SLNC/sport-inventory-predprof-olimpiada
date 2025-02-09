from pydantic import BaseModel
from src.schemas.appl_schemas import ApplicationsDTO


class UsersLoginDTO(BaseModel):
    username: str
    password: str
    role: str


class UsersAddDTO(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    second_lastname: str


class UsersUpdDTO(BaseModel):
    firstname: str
    lastname: str
    second_lastname: str


class UsersDTO(BaseModel):
    username: str
    firstname: str
    lastname: str
    second_lastname: str
    applications: list[ApplicationsDTO]

    class Config:
        orm_mode = True
        from_attributes = True

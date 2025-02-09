from pydantic import BaseModel
from src.models import ApplStatus
import datetime


# Класс для валидации данных о заявках при их добавлении.
class ApplicationsAddDTO(BaseModel):
    inventory_id: int
    count: int


# Класс для валидации данных о заявках при их отображении.
class ApplicationsDTO(ApplicationsAddDTO):
    id: int
    user_id: str
    created_at: datetime.datetime
    closed_at: datetime.datetime | None
    status: ApplStatus
    inventory_name: str
    comment: str | None

    class Config:
        orm_mode = True
        from_attributes = True


# Класс для валидации данных о заявках при их добавлении.
class ApplicationsCommentDTO(BaseModel):
    application_id: int
    comment: str | None
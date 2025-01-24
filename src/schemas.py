from datetime import datetime
from typing import Optional
import src.models
from src.database import str_256
from pydantic import BaseModel, ConfigDict


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

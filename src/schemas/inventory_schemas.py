from typing import Optional
from pydantic import BaseModel


# Класс для валидации данных об инвентаре при их добавлении.
class InventoryAddDTO(BaseModel):
    name: str
    count_new: Optional[int]
    count_broken: Optional[int]
    count_inuse: Optional[int]


# Класс для валидации данных об инвентаре  при их отображении.
class InventoryDTO(InventoryAddDTO):
    id: int


# Класс для обновления информации об инвентаре.
class InventoryUpdDTO(InventoryAddDTO):
    id: int

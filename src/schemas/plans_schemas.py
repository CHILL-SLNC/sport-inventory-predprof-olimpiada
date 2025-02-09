from pydantic import BaseModel


class PurchPlansAddDTO(BaseModel):
    inventory_id: int
    count: int
    cost: int
    provider: str

    class Config:
        orm_mode = True
        from_attributes = True


class PurchPlansDTO(PurchPlansAddDTO):
    id: int
    admin_id: str
    inventory_name: str

    class Config:
        orm_mode = True
        from_attributes = True

from pydantic import BaseModel

class OrderCreate(BaseModel):
    item: str
    quantity: int


class OrderResponse(BaseModel):
    id: int
    item: str
    quantity: int

    class Config:
        from_attributes = True

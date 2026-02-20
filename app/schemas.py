from app.models import OrderStatus

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderCreate(BaseModel):
    item: str
    quantity: int


class OrderResponse(BaseModel):
    id: int
    item: str
    quantity: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    item : Optional[str] = None
    quantity : Optional[int] = None
    
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.order import OrderCreate, OrderResponse
from app.database import get_db
from app.models.order import Order
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(item=order.item, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    return order






from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import engine, Base, get_db
from app.schemas import OrderCreate, OrderResponse, OrderUpdate
from app.models import Order, OrderStatus


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(item=order.item, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        ) 
    db.delete(order)
    db.commit()
    return {'detail': "Deleted successfully"}


@app.patch("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_data.item is None and order_data.quantity is None:
        raise HTTPException(status_code=400, detail="Put some data in it")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Order cannot be updated in current status")

    if order_data.item is not None:
        order.item = order_data.item

    if order_data.quantity is not None:
        order.quantity = order_data.quantity

    

    db.commit()
    db.refresh(order)
    return order
    
    
        


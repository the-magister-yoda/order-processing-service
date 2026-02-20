from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from functools import wraps

from app.database import engine, Base, get_db
from app.schemas import OrderCreate, OrderResponse, OrderUpdate
from app.models import Order, OrderStatus
from app.services.order_service import service_update_order, service_process_order, service_complete_order, service_fail_order
from app.errors import OrderNotFound, OrderEmpty, InvalidStatus


app = FastAPI()
Base.metadata.create_all(bind=engine)


def handle_order_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OrderNotFound:
            raise HTTPException(status_code=404, detail="Order Not Found")
        except InvalidStatus:
            raise HTTPException(status_code=400, detail="Order cannot be updated in current status")
        except OrderEmpty:
            raise HTTPException(status_code=400, detail="Put some data in it")
    return wrapper



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
@handle_order_errors
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    return service_update_order(order_id, order_data, db)


@app.post("/orders/{order_id}/process", response_model=OrderResponse)
@handle_order_errors
def process_order(order_id: int, db: Session = Depends(get_db)):
    return service_process_order(order_id, db)
    

@app.post("/orders/{order_id}/complete", response_model=OrderResponse)
@handle_order_errors
def complete_order(order_id: int, db: Session = Depends(get_db)):
    return service_complete_order(order_id, db)


@app.post("/orders/{order_id}/fail", response_model=OrderResponse)
@handle_order_errors
def fail_order(order_id: int, db: Session = Depends(get_db)):
    return service_fail_order(order_id, db)

    
    


        
    
    
        


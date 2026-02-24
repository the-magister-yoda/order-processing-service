from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functools import wraps
from typing import List

from database import Base, engine, get_db
from models import Order
from schemas import OrderCreate, OrderResponse, OrderUpdate
from errors import OrderNotFound, OrderEmpty, InvalidStatus
from app.services.order_service import service_create_order, service_get_orders, service_get_order, service_delete_order, service_update_order
from app.services.order_service import service_process_order, service_complete_order, service_fail_order


router = APIRouter()


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


@router.post("/", response_model=OrderResponse)
@handle_order_errors
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return service_create_order(order, db)


@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return service_get_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
@handle_order_errors
def get_order(order_id: int, db: Session = Depends(get_db)):
    return service_get_order(order_id, db)


@router.delete("/{order_id}")
@handle_order_errors
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return service_delete_order(order_id, db)


@router.patch("/{order_id}", response_model=OrderResponse)
@handle_order_errors
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    return service_update_order(order_id, order_data, db)


@router.post("/{order_id}/process", response_model=OrderResponse)
@handle_order_errors
def process_order(order_id: int, db: Session = Depends(get_db)):
    return service_process_order(order_id, db)
    

@router.post("/{order_id}/complete", response_model=OrderResponse)
@handle_order_errors
def complete_order(order_id: int, db: Session = Depends(get_db)):
    return service_complete_order(order_id, db)


@router.post("/{order_id}/fail", response_model=OrderResponse)
@handle_order_errors
def fail_order(order_id: int, db: Session = Depends(get_db)):
    return service_fail_order(order_id, db)

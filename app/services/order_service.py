from app.errors import OrderNotFound, OrderEmpty, InvalidStatus
from app.models import Order, OrderStatus


def service_update_order(order_id, order_data, db):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise OrderNotFound()
    
    if order_data.item is None and order_data.quantity is None:
        raise OrderEmpty()

    if order.status != OrderStatus.PENDING:
        raise InvalidStatus()

    if order_data.item is not None:
        order.item = order_data.item

    if order_data.quantity is not None:
        order.quantity = order_data.quantity

    db.commit()
    db.refresh(order)
    return order


def service_process_order(order_id, db):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise OrderNotFound()

    if order.status != OrderStatus.PENDING:
        raise InvalidStatus()

    order.status = OrderStatus.PROCESSING

    db.commit()
    db.refresh(order)
    return order


def service_complete_order(order_id, db):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise OrderNotFound()

    if order.status != OrderStatus.PROCESSING:
        raise InvalidStatus()

    order.status = OrderStatus.COMPLETED

    db.commit()
    db.refresh(order)
    return order


def service_fail_order(order_id, db):
    order = db.query(Order).filter(order.id == order_id).first()

    if order is None:
        raise OrderNotFound()

    if order.status != OrderStatus.PROCESSING:
        raise InvalidStatus()

    order.status = OrderStatus.FAILED

    db.commit()
    db.refresh(order)
    return order

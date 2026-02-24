from errors import OrderNotFound, OrderEmpty, InvalidStatus, 
from models import Order, OrderStatus
from app.tasks.order_tasks import process_order_task


def service_create_order(order, db):
    db_order = Order(item=order.item, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def service_get_orders(db):
    orders = db.query(Order).all()
    if orders is None:
        raise OrderNotFound()
    return orders


def service_get_order(order_id, db):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise OrderNotFound()

    return order

    
def service_delete_order(order_id, db):
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise OrderNotFound()
    
    db.delete(order)
    db.commit()
    return {'detail': "Deleted successfully"}



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

    process_order_task.delay(order_id)

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
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise OrderNotFound()

    if order.status != OrderStatus.PROCESSING:
        raise InvalidStatus()

    order.status = OrderStatus.FAILED

    db.commit()
    db.refresh(order)
    return order




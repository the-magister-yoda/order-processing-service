import time

from app.celery_app import celery_app
from models import Order, OrderStatus
from database import SessionLocal
from app.utils.email import send_email


@celery_app.task(bind=True, max_retries=3)
def process_order_task(self, order_id: int):
    db = SessionLocal()

    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            return

        print(f"Обработка заказа {order_id} началась")

        time.sleep(5)  # имитация тяжёлой работы

        order.status = OrderStatus.COMPLETED
        db.commit()

        # 🔥 Отправляем email
        send_email(
            to_email="specialforgoodpurpose@mail.ru",
            subject="Заказ завершён",
            body=f"Ваш заказ №{order_id} успешно обработан."
        )

        print(f"Заказ {order_id} завершён и email отправлен")

    except Exception as e:
        db.rollback()

        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = OrderStatus.FAILED
            db.commit()

        print(f"Ошибка: {e}")

        # retry через 5 секунд
        raise self.retry(exc=e, countdown=5)

    finally:
        db.close()

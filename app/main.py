from fastapi import FastAPI
from app.routers import orders
from app.database import engine, Base


app = FastAPI()


app.include_router(orders.router, prefix="/orders")


Base.metadata.create_all(bind=engine)


from fastapi import FastAPI
from app.routers import orders, users
from app.database import Base, engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(orders.router, prefix="/orders")
app.include_router(users.router, prefix="/users")



    
    


        
    
    
        


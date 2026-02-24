from fastapi import FastAPI
from app.routers import orders, users


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(orders.router, prefix="/orders")
app.include_router(users.router, prefix="/users")



    
    


        
    
    
        


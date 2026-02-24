from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from functools import wraps
from typing import List

from errors import UserNotFound, EmailAlreadyExists, InvalidStatus, WrongPassword
from database import engine, Base, get_db
from schemas import UserCreate, UserResponse
from models import User
from app.services.user_service import service_create_user, service_login_user


router = APIRouter()


def handle_user_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UserNotFound:
            raise HTTPException(status_code=404, detail="User not found try again")
        except InvalidStatus:
            raise HTTPException(status_code=400, detail="Order cannot be updated in current status")
        except EmailAlreadyExists:
            raise HTTPException(status_code=400, detail="This email already taken")
        except WrongPassword:
            raise HTTPException(status_code=400, detail="Oops Wrong password try again")
    return wrapper


@router.post("/create", response_model=UserResponse)
@handle_user_errors
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return service_create_user(user, db) 


@router.post("/login")
@handle_user_errors
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    return service_login_user(user, db)



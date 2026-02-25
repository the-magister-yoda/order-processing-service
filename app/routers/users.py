from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from functools import wraps
from typing import List

from app.errors import UserNotFound, EmailAlreadyExists, InvalidStatus, WrongPassword
from app.database import engine, Base, get_db
from app.schemas import UserCreate, UserResponse, TokenResponse
from app.models import User
from app.services.user_service import service_register_user, service_login_user


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


@router.post("/register", response_model=UserResponse)
@handle_user_errors
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return service_register_user(user, db) 


@router.post("/login", response_model=TokenResponse)
@handle_user_errors
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    return service_login_user(user, db)



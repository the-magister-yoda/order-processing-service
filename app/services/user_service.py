from sqlalchemy.exc import IntegrityError

from app.errors import InvalidStatus, EmailAlreadyExists, UserNotFound, WrongPassword
from app.models import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token


def service_register_user(user, db):
    is_email_taken = db.query(User).filter(User.email == user.email).first()

    if is_email_taken is not None:
        raise EmailAlreadyExists()

    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExists()

    db.refresh(db_user)
    return db_user
    

def service_login_user(user, db):
    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user is None:
        raise UserNotFound()

    if not verify_password(user.password, db_user.hashed_password):
        raise WrongPassword()
    
    access_token = create_access_token(
        data={"sub": str(db_user.id), "role": db_user.role.value}
    )

    return {"access_token": access_token, "token_type": "bearer"}
    


    

    
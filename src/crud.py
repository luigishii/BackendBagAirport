import logging
from sqlalchemy.orm import Session
from src import models, schemas
from src.security import hash_password, verify_password
from fastapi import HTTPException, status

def create_user(db: Session, user: schemas.UserCreate):
    logging.info(f"Attempting to create user with username: {user.username} and email: {user.email}")
    db_user = models.User(username=user.username,
                          email=user.email,
                          hashed_password=hash_password(user.hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logging.info(f"User created successfully with ID: {db_user.id}")
    return db_user

def get_user(user_id: int, db: Session):
    logging.info(f"Fetching user with ID: {user_id}")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        logging.info(f"User found with ID: {user_id}")
    else:
        logging.warning(f"No user found with ID: {user_id}")
    return user

def update_user(user_id: int, new_password: str, db: Session) -> models.User:
    logging.info(f"Attempting to update password for user with ID: {user_id}")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.hashed_password = hash_password(new_password)
        db.commit()
        db.refresh(db_user)
        logging.info(f"Password updated successfully for user with ID: {user_id}")
        return db_user
    else:
        logging.warning(f"No user found with ID: {user_id} to update")
        return None

def delete_user(db: Session, user_id: int):
    logging.info(f"Attempting to delete user with ID: {user_id}")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        logging.info(f"User deleted successfully with ID: {user_id}")
        return db_user
    else:
        logging.warning(f"No user found with ID: {user_id} to delete")
        return None

def login(db: Session, email: str, password: str):
    logging.info(f"Attempting to log in with email: {email}")
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        if verify_password(password, user.hashed_password):
            logging.info(f"Login successful for email: {email}")
            return user
        else:
            logging.warning(f"Invalid password for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        logging.warning(f"No user found with email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
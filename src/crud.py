from sqlalchemy.orm import Session
from src import models, schemas
from .models import User
from .schemas import UserCreate
from src.security import hash_password, verify_password
from fastapi import HTTPException, status

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username,
        email=user.email,
        hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(user_id: int, new_password: str, db: Session) -> models.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.hashed_password = hash_password(new_password)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

def login(db: Session, email: str, password: str):
    # Procura o usuário no banco de dados pelo email
    user = db.query(models.User).filter(models.User.email == email).first()
    
    # Se o usuário não for encontrado, levanta uma exceção
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se a senha fornecida corresponde ao hash da senha armazenada
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

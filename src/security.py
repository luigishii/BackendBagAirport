from sqlalchemy.orm import Session
from src.models import schemas
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from src.database.db import get_db
from fastapi import HTTPException,Depends,status

from src.models import models

# Configuração do contexto de hashing de senhas
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

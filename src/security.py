from sqlalchemy.orm import Session
from src import models, schemas
from passlib.context import CryptContext

# Configuração do contexto de hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
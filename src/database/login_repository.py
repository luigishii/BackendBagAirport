from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models import schemas
from src.database import get_db
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from src.models import models  # Importando datetime e timedelta

router = APIRouter()

# Crie um contexto de hash para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Defina suas constantes de chave secreta e algoritmo
SECRET_KEY = "seu_secret_key_aqui"  # Obtenha isso do seu .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiração do token em minutos

    
# Função para gerar o token de acesso
def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





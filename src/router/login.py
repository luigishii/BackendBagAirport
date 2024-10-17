from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models import models, schemas
from src.security import verify_password
from src.database.token import create_access_token  # Agora importado do novo arquivo

app = APIRouter()

@app.post("/login", tags=["user"])
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == request.email).first()
    
    if user is None or not verify_password(request.password, user.senha):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    
    access_token = create_access_token(data={"sub": user.idUsuario})
    
    # Retorne o userId e o nome do usuário junto com o token de acesso
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "userId": user.idUsuario,
        "userName": user.nome  # Adicione esta linha para retornar o nome do usuário
    }

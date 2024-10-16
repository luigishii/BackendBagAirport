from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.models import models
from src.security import verify_password
from src.database.token import create_access_token  # Agora importado do novo arquivo

app = APIRouter()

@app.post("/login",tags=["user"])
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if user is None or not verify_password(password, user.senha):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")

    access_token = create_access_token(data={"sub": user.idUsuario})
    return {"access_token": access_token, "token_type": "bearer"}

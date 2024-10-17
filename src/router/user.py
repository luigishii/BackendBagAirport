from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src import crud
from src.database.db import get_db
from src.database.user_repository import get_all_users
from src.models import models, schemas

app = APIRouter()

@app.post("/v1/users", tags=["user"], response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", tags=["user"], response_model=schemas.UserGet)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(user_id, db=db)

@app.put("/users/{user_id}" ,tags=["user"], response_model=schemas.UserBase)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(user_id, user_update.new_password, db)

@app.delete("/users/{user_id}",tags=["user"], response_model=dict)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)

@app.get("/users",tags=["user"], response_model=list[schemas.UserGet])
def list_all_users(db: Session = Depends(get_db)):
    """
    Rota para listar todos os usuários do banco de dados.
    """
    return get_all_users(db)
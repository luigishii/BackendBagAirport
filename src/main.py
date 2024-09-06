from fastapi import FastAPI, Depends, HTTPException
from src import crud, models, schemas
from src.database import engine
from fastapi.middleware.cors import CORSMiddleware
from src.database import get_db
from sqlalchemy.orm import Session

# Cria o banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(user_id, db=db)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(user_id, user_update.new_password, db)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/login", response_model=schemas.User)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.login(db, email, password)
    return user
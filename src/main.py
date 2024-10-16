from datetime import datetime
import logging
import os
from fastapi import FastAPI, Depends, HTTPException, status
from src import crud, models, schemas
from src.crud import create_mala_function, is_admin_user, excluir_mala, excluir_tag
from src.database import engine
from fastapi.middleware.cors import CORSMiddleware
from src.database import get_db
from sqlalchemy.orm import Session
from src.login import create_access_token
from src.security import verify_password
from sqlalchemy.exc import NoResultFound

# Cria o banco de dados
models.Base.metadata.create_all(bind=engine)

def setup_logging():
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file = os.path.join(log_directory, f'{datetime.now().strftime("%Y-%m-%d")}.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

setup_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/", response_model=schemas.UserBase)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.UserGet)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(user_id, db=db)

@app.put("/users/{user_id}", response_model=schemas.UserBase)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(user_id, user_update.new_password, db)

@app.delete("/users/{user_id}", response_model=dict)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)


@app.post("/mala/")
def create_mala_route(mala: schemas.MalaCreate, user_id: int, db: Session = Depends(get_db)):
    # Busca o usuário no banco de dados
    user = db.query(models.Usuario).filter(models.Usuario.idUsuario == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se o usuário é administrador
    if not is_admin_user:  # Altere para verificar a propriedade 'isAdmin' do usuário
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar esta ação.",
        )

    # Se tudo estiver correto, chama a função para criar a mala
    return create_mala_function(mala, db, user)

@app.delete("/mala/{mala_id}", response_description="Exclui uma mala pelo ID")
def delete_mala(mala_id: int, db: Session = Depends(get_db)):
    """
    Exclui uma mala do banco de dados e a tag relacionada.

    :param mala_id: O ID da mala a ser excluída.
    :param db: A sessão do banco de dados.
    :raises HTTPException: Se a mala ou a tag não forem encontradas.
    """
    try:
        # Obtenha a mala antes de excluir para saber a tag relacionada
        mala = db.query(models.Mala).filter(models.Mala.id == mala_id).one()
        
        # Armazene o idTag da mala para exclusão posterior
        id_tag = mala.idTag

        # Exclua a mala
        resultado = excluir_mala(db, mala_id)
        
        # Exclua a tag relacionada
        excluir_tag(db, id_tag)  # Presumindo que `excluir_tag` é uma função que exclui a tag pelo idTag

        return {"message": resultado}
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Mala com ID {mala_id} não encontrada.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if user is None or not verify_password(password, user.senha):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    
    # Lógica para gerar o token de acesso
    access_token = create_access_token(data={"sub": user.idUsuario})
    return {"access_token": access_token, "token_type": "bearer"}


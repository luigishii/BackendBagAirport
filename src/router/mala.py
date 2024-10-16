from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from src.models import schemas
from src.crud import excluir_tag, is_admin_user
from src.database.mala_repository import create_mala_function, excluir_mala
from src.database.db import get_db
from sqlalchemy.exc import NoResultFound

from src.models import models

app = APIRouter()

@app.post("/mala/", tags=["mala"])
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

@app.delete("/mala/{mala_id}",tags=["mala"], response_description="Exclui uma mala pelo ID")
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
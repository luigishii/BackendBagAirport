import logging
from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from src.models import schemas
from src.models import models
from src.security import hash_password, verify_password
from fastapi import HTTPException, status

#ADMIN

def is_admin_user(user: models.Usuario):
    if not user.isAdmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar essa ação."
        )
        


def excluir_tag(db: Session, tag_id: int):
    """
    Exclui uma tag pelo ID fornecido.

    :param db: A sessão do banco de dados.
    :param tag_id: O ID da tag a ser excluída.
    :raises NoResultFound: Se a tag não for encontrada.
    """
    tag = db.query(models.TagRFID).filter(models.TagRFID.idTag == tag_id).one() 
    db.delete(tag)
    db.commit()
    return f"Tag com ID {tag_id} excluída com sucesso."


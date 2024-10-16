from fastapi import HTTPException,status
from requests import Session
from src.models import schemas
from src.models import models



def create_mala_function(mala: schemas.MalaCreate, db: Session, current_user: models.Usuario):
    # Verifica se o usuário é um administrador
    if not current_user.isAdmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar essa ação."
        )
    
    # Verifica se a tag já existe
    tag = db.query(models.TagRFID).filter(models.TagRFID.idTag == mala.idTag).first()

    if tag is None:
        # Cria uma nova tag se não existir
        nova_tag = models.TagRFID(
            idTag=mala.idTag,  # Presumindo que idTag é o identificador único
            descricaoTag=mala.descricaoTag,  # Descrição da tag
            # Adicione outros campos conforme necessário
        )
        db.add(nova_tag)
        db.commit()
        db.refresh(nova_tag)

    # Agora, cria a mala
    nova_mala = models.Mala(
        idTag=mala.idTag,  # Usa o idTag da tag criada ou existente
        descricaoTag=mala.descricaoTag,
        statusLocalizacao=mala.statusLocalizacao,
        verificacaoEntrega=mala.verificacaoEntrega
    )

    db.add(nova_mala)
    db.commit()
    db.refresh(nova_mala)

    return nova_mala


def excluir_mala(session: Session, mala_id: int):
    """
    Exclui uma mala do banco de dados com base no ID fornecido.

    :param session: A sessão do SQLAlchemy para interagir com o banco de dados.
    :param mala_id: O ID da mala a ser excluída.
    :raises NoResultFound: Se a mala não for encontrada.
    """
    mala = session.query(models.Mala).filter(models.Mala.id == mala_id).first()
    
    if mala is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mala não encontrada."
        )
    
    session.delete(mala)
    session.commit()
    return f"Mala com ID {mala_id} excluída com sucesso."
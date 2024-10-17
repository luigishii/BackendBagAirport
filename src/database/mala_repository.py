import logging
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

    # Se a tag não existir, cria uma nova tag
    if tag is None:
        nova_tag = models.TagRFID(
            descricaoTag=mala.descricaoTag,  # Descrição da tag
            # Adicione outros campos conforme necessário
        )
        db.add(nova_tag)
        db.commit()
        db.refresh(nova_tag)
        idTag = nova_tag.idTag  # Pega o idTag da nova tag criada
    else:
        idTag = tag.idTag  # Usa o idTag da tag existente

    # Agora, cria a mala
    nova_mala = models.Mala(
        idTag=idTag,  # Usa o idTag da tag criada ou existente
        idUsuario=current_user.idUsuario,  # Define o idUsuario do usuário atual
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

def get_user_bags_history(user_id: int, db: Session) -> list[schemas.Mala]:
    """
    Função para obter o histórico de malas de um usuário.
    
    :param user_id: ID do usuário.
    :param db: Sessão do banco de dados.
    :return: Lista com o histórico de malas.
    """
    logging.info(f"Buscando histórico de malas para o usuário com ID: {user_id}")
    
    # Buscar o usuário no banco de dados
    user = db.query(models.Usuario).filter(models.Usuario.idUsuario == user_id).first()
    
    if not user:
        logging.warning(f"Nenhum usuário encontrado com ID: {user_id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Buscar o histórico de malas associadas ao usuário
    bags_history = db.query(models.Mala).filter(models.Mala.idUsuario == user_id).all()

    if bags_history:
        logging.info(f"Foram encontradas {len(bags_history)} malas para o usuário com ID: {user_id}")
        return [schemas.Mala(
            idMala=bag.id,  # Usando o atributo correto do modelo
            descricao=bag.descricaoTag,
            status=bag.statusLocalizacao,
        ) for bag in bags_history]
    else:
        logging.warning(f"Nenhuma mala encontrada para o usuário com ID: {user_id}")
        return []


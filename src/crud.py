import logging
from sqlite3 import IntegrityError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src import models, schemas
from src.security import hash_password, verify_password
from fastapi import HTTPException, status

#USER

# Função para criar um novo usuário
def create_user(db: Session, user: schemas.UserCreate):
    logging.info(f"Attempting to create user with email: {user.email}")
    
    try:
        # Cria um novo usuário com os dados fornecidos
        db_user = models.Usuario(
            nome=user.nome,
            email=user.email,
            telefone=user.telefone,
            senha=hash_password(user.senha),
            isAdmin=user.isAdmin
        )
        db.add(db_user)  # Adiciona o usuário no banco de dados
        db.commit()  # Confirma a transação
        db.refresh(db_user)  # Atualiza a instância do usuário
        logging.info(f"User created successfully with ID: {db_user.idUsuario}")
        
        # Retorna um dicionário que corresponde ao modelo UserBase
        return schemas.UserBase(
            nome=db_user.nome,
            email=db_user.email,
            telefone=db_user.telefone,
            senha=db_user.senha,  
            isAdmin=db_user.isAdmin
        )
    except IntegrityError as e:
        db.rollback()  # Desfaz a transação em caso de erro
        logging.error(f"IntegrityError while creating user: {e}")
        if 'unique constraint' in str(e):  # Verifica se o erro foi causado por violação de constraint única
            raise HTTPException(status_code=400, detail="Email ou telefone já estão em uso.")
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário.")
    except Exception as e:
        db.rollback()
        logging.error(f"Unexpected error while creating user: {e}")
        raise HTTPException(status_code=500, detail="Erro inesperado ao criar usuário.")


def get_user(user_id: int, db: Session) -> schemas.UserGet:
    logging.info(f"Fetching user with ID: {user_id}")
    user = db.query(models.Usuario).filter(models.Usuario.idUsuario == user_id).first()
    
    if user:
        logging.info(f"User found with ID: {user_id}")
        return schemas.UserGet(
            id=user.idUsuario,
            nome=user.nome,
            email=user.email,
            telefone=user.telefone,
            isAdmin=user.isAdmin
        )
    else:
        logging.warning(f"No user found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")


# Função para atualizar a senha de um usuário
def update_user(user_id: int, new_password: str, db: Session) -> schemas.UserBase:
    logging.info(f"Attempting to update password for user with ID: {user_id}")
    db_user = db.query(models.Usuario).filter(models.Usuario.idUsuario == user_id).first()
    if db_user:
        db_user.senha = hash_password(new_password)  # Atualiza a senha com a versão hash
        db.commit()  # Confirma a transação
        db.refresh(db_user)  # Atualiza a instância do usuário
        logging.info(f"Password updated successfully for user with ID: {user_id}")

        # Retorne uma nova instância de UserBase
        return schemas.UserBase(
            nome=db_user.nome,
            email=db_user.email,
            telefone=db_user.telefone,
            senha=db_user.senha,  
            isAdmin=db_user.isAdmin
        )
    else:
        logging.warning(f"No user found with ID: {user_id} to update")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

# Função para deletar um usuário
def delete_user(db: Session, user_id: int):
    logging.info(f"Attempting to delete user with ID: {user_id}")
    db_user = db.query(models.Usuario).filter(models.Usuario.idUsuario == user_id).first()
    if db_user:
        db.delete(db_user)  # Deleta o usuário
        db.commit()  # Confirma a transação
        logging.info(f"User deleted successfully with ID: {user_id}")
        return {"detail": "Usuário deletado com sucesso."}  # Mensagem de confirmação
    else:
        logging.warning(f"No user found with ID: {user_id} to delete")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

#reserva
def login(db: Session, email: str, password: str) -> dict:
    logging.info(f"Attempting to log in with email: {email}")
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if user:
        if verify_password(password, user.senha):  # Verifica se a senha está correta
            logging.info(f"Login successful for email: {email}")
            return {
                "detail": "Usuário logado com sucesso.",
                "isAdmin": user.isAdmin  # Inclui o valor de isAdmin no retorno
            }
        else:
            logging.warning(f"Invalid password for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        logging.warning(f"No user found with email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

#ADMIN

def is_admin_user(user: models.Usuario):
    if not user.isAdmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para realizar essa ação."
        )
        

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

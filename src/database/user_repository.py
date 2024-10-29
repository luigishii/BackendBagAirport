import logging
from sqlite3 import IntegrityError
from typing import List
from sqlalchemy.orm import Session
from src.models import schemas
from src.models import models
from src.security import hash_password
from fastapi import HTTPException, status


def create_user(db: Session, user: schemas.UserCreate):
    logging.info(f"Attempting to create user with email: {user.email}")
    
    try:
        # Verifica se role está presente, se não, define um padrão
        role = user.role.lower() if hasattr(user, 'role') else 'traveler'

        # Cria um novo usuário com os dados fornecidos
        db_user = models.Usuario(
            nome=user.nome,
            email=user.email,
            telefone=user.telefone,
            senha=hash_password(user.senha),
            isAdmin=user.isAdmin,
            role=role  # Inclui o campo role
        )
        db.add(db_user)  # Adiciona o usuário no banco de dados
        db.commit()  # Confirma a transação
        db.refresh(db_user)  # Atualiza a instância do usuário
        logging.info(f"User created successfully with ID: {db_user.idUsuario}")
        
        return schemas.UserBase(
            nome=db_user.nome,
            email=db_user.email,
            telefone=db_user.telefone,
            senha=db_user.senha,  
            isAdmin=db_user.isAdmin,
            role=db_user.role
        )
    except IntegrityError as e:
        db.rollback()  # Desfaz a transação em caso de erro
        logging.error(f"IntegrityError while creating user: {e}")
        if 'unique constraint' in str(e):
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
            isAdmin=user.isAdmin,
            role=user.role
        )
    else:
        logging.warning(f"No user found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
def get_all_users(db: Session) -> List[schemas.UserGet]:
    logging.info("Fetching all users")
    users = db.query(models.Usuario).all()

    if users:
        logging.info(f"Found {len(users)} users")
        return [schemas.UserGet(
            id=user.idUsuario,
            nome=user.nome,
            email=user.email,
            telefone=user.telefone,
            isAdmin=user.isAdmin,
            role=user.role
        ) for user in users]
    else:
        logging.warning("No users found")
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado.")



# Função para atualizar a senha de um usuário
def update_senha(user_id: int, new_password: str, db: Session) -> schemas.UserBase:
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
            isAdmin=db_user.isAdmin,
            role=db_user.role
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
    
    
    
def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session) -> schemas.UserBase:
    logging.info(f"Attempting to update user with ID: {user_id}")
    
    # Busca o usuário no banco de dados
    db_user = db.query(models.Usuario).filter(models.Usuario.idUsuario == user_id).first()
    
    if db_user:
        # Atualiza os dados do usuário
        db_user.nome = user_data.nome
        db_user.email = user_data.email
        db_user.telefone = user_data.telefone
        
        # Atualiza a senha apenas se uma nova senha for fornecida
        if user_data.senha:  # Isso só funcionará se `senha` estiver no modelo
            db_user.senha = hash_password(user_data.senha)  # Atualiza a senha com a versão hash
        
        db_user.isAdmin = user_data.isAdmin
        db_user.role = user_data.role
                
        db.commit()  # Confirma a transação
        db.refresh(db_user)  # Atualiza a instância do usuário
        logging.info(f"User updated successfully with ID: {user_id}")

        # Retorna uma nova instância de UserBase
        return schemas.UserBase(
            nome=db_user.nome,
            email=db_user.email,
            telefone=db_user.telefone,
            senha=db_user.senha,  # Retorna a senha, mas considere não retornar senhas por motivos de segurança
            isAdmin=db_user.isAdmin,
            role=db_user.role
        )
    else:
        logging.warning(f"No user found with ID: {user_id} to update")
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
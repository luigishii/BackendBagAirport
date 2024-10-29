from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Enum

class UserRole(str, Enum):
    collaborator = "Collaborator"
    admin = "Admin"
    traveler = "Traveler"
    other = "Other"

class UserBase(BaseModel):
    nome: str
    email: str
    telefone: str
    senha: Optional[str] = None
    isAdmin: bool
    role: UserRole
    
class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    nome: str
    email: str
    telefone: str
    senha: str | None = None  # Torne a senha opcional
    isAdmin: bool
    role: UserRole

    
class UserUpdatePassword(BaseModel):
    new_password: str

class UserGet(BaseModel):
    nome: str
    email: str
    telefone: str
    isAdmin: bool
    role: UserRole


    class Config:
        orm_mode = True
        
class Mala(BaseModel):
    idMala: int
    descricao: str
    status: str

    class Config:
        orm_mode = True
        
class MalaCreate(BaseModel):
    idTag: int
    descricaoTag: str
    statusLocalizacao: str = None
    verificacaoEntrega: bool = False
    
class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
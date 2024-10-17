from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    nome: str
    email: str
    telefone: str
    senha:str
    isAdmin: bool
    
class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    new_password: str

class UserGet(BaseModel):
    nome: str
    email: str
    telefone: str
    isAdmin: bool


    class Config:
        orm_mode = True
        
class Mala(BaseModel):
    idMala: int
    descricao: str
    status: str
    ultima_localizacao: str
    data_criacao: datetime

    class Config:
        orm_mode = True
        
class MalaCreate(BaseModel):
    idTag: int
    descricaoTag: str
    statusLocalizacao: str = None
    verificacaoEntrega: bool = False
    
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
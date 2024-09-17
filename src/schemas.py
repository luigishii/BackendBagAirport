from typing import Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str
    email: str
    cpf: str
    hashed_password:str
    
class UserCreate(UserBase):
    username: str
    email: str
    cpf: Optional[str] = Field(None, description="Cadastro de Pessoa Física")
    hashed_password:str

class UserUpdate(BaseModel):
    new_password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
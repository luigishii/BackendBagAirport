from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    hashed_password:str
    
class UserCreate(UserBase):
    username: str
    email: str
    hashed_password:str

class UserUpdate(BaseModel):
    new_password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
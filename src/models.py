from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
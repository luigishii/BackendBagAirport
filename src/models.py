from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    cpf = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
    
class Mala(Base):
    __tablename__ = 'mala'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # SERIAL é simulado por autoincrement=True
    rfid = Column(String, unique=True, index=True)
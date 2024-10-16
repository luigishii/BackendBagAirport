from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    idUsuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=True)
    senha = Column(String, nullable=False)
    isAdmin = Column(Boolean, default=False)

class LeitorRFID(Base):
    __tablename__ = 'leitor_rfid'
    
    idLeitor = Column(Integer, primary_key=True, autoincrement=True)
    localizacao = Column(String, nullable=False)
    status = Column(Boolean, default=True)

class TagRFID(Base):
    __tablename__ = 'tag_rfid'
    
    idTag = Column(Integer, primary_key=True, autoincrement=True)
    descricaoTag = Column(String, index=True)
    
class Mala(Base):
    __tablename__ = 'mala'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    idTag = Column(Integer, ForeignKey('tag_rfid.idTag'), nullable=False)
    descricaoTag = Column(String, nullable=False)
    statusLocalizacao = Column(String, nullable=True)
    verificacaoEntrega = Column(Boolean, default=False)
    
    tag_rfid = relationship("TagRFID")

# Tabela Viagem
class Viagem(Base):
    __tablename__ = 'viagem'
    
    idViagem = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String, nullable=False)



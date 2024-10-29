from sqlalchemy import Column, Enum, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base

class UserRoledb(str, Enum):
    collaborator = "collaborator"
    admin = "admin"
    traveler = "traveler"
    other = "other"

class Usuario(Base):
    __tablename__ = 'usuario'
    
    idUsuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=True)
    senha = Column(String, nullable=False)
    isAdmin = Column(Boolean, default=False)
    # Usando uma tupla de strings diretamente no Enum do SQLAlchemy
    role = Column(Enum("collaborator", "admin", "traveler", "other", name="userrole_enum"), nullable=False)
    
    malas = relationship("Mala", back_populates="usuario")

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
    idUsuario = Column(Integer, ForeignKey('usuario.idUsuario'), nullable=False)  # Associa Mala ao Usuario
    descricaoTag = Column(String, nullable=False)
    statusLocalizacao = Column(String, nullable=True)
    verificacaoEntrega = Column(Boolean, default=False)
    
    tag_rfid = relationship("TagRFID")
    usuario = relationship("Usuario", back_populates="malas")  # Relacionamento com Usuario

# Tabela Viagem
class Viagem(Base):
    __tablename__ = 'viagem'
    
    idViagem = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String, nullable=False)

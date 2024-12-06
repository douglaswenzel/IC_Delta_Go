from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    user_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    sobrenome = Column(String, index=True)
    tipo = Column(String)
    nascimento = Column(Date)
    unidade = Column(String)
    observacoes = Column(String, nullable=True)
    permissao = Column(Boolean)
    pasta_id = Column(Integer)
    aluno = relationship("Aluno", back_populates="usuario", uselist=False)
    funcionario = relationship("Funcionario", back_populates="usuario", uselist=False)
    visitante = relationship("Visitante", back_populates="usuario", uselist=False)
    aluno = relationship('Aluno', back_populates='usuario', uselist=False)


class Aluno(Base):
    __tablename__ = 'aluno'

    aluno_id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String, unique=True, index=True)
    curso = Column(String)
    turma = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuario.user_id'))

    usuario = relationship("Usuario", back_populates="aluno")


class Funcionario(Base):
    __tablename__ = 'funcionario'

    funcionario_id = Column(Integer, primary_key=True, index=True)
    cargo = Column(String)
    setor = Column(String)
    data_admissao = Column(Date)
    usuario_id = Column(Integer, ForeignKey('usuario.user_id'))

    usuario = relationship("Usuario", back_populates="funcionario")


class Visitante(Base):
    __tablename__ = 'visitante'

    visitante_id = Column(Integer, primary_key=True, index=True)
    motivo_visita = Column(String)
    visitado = Column(String)
    data_visita = Column(Date)
    usuario_id = Column(Integer, ForeignKey('usuario.user_id'))

    usuario = relationship("Usuario", back_populates="visitante")

class Pasta(Base):
    __tablename__ = 'pasta'

    pasta_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    caminho = Column(String)

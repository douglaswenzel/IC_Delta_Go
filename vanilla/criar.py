from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Aluno(Base):
    __tablename__ = 'aluno'

    aluno_id = Column(Integer, primary_key=True)
    matricula = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    turma = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.user_id'))


class Usuario(Base):
    __tablename__ = 'usuario'

    user_id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)


engine = create_engine('mysql+mysqlconnector://dougl947_user:User24!e@162.241.2.230:3306/dougl947_DeltaGo')

Base.metadata.create_all(engine)

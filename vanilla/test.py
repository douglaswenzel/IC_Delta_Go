from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'mysql+mysqlconnector://dougl947_user:User24!e@162.241.2.230:3306/dougl947_DeltaGo'

Base = declarative_base()


# Definindo a classe Usuario
class Usuario(Base):
    __tablename__ = 'usuario'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    nascimento = Column(Date, nullable=False)
    unidade = Column(String(100), nullable=False)
    observacoes = Column(Text, nullable=True)
    permissao = Column(Boolean, nullable=False)

    aluno = relationship('Aluno', back_populates='usuario', uselist=False)
    visitante = relationship('Visitante', back_populates='usuario', uselist=False)


class Aluno(Base):
    __tablename__ = 'aluno'

    aluno_id = Column(Integer, primary_key=True, autoincrement=True)
    matricula = Column(String(255), nullable=False)
    curso = Column(String(255), nullable=False)
    turma = Column(String(255), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.user_id', ondelete='SET NULL', onupdate='CASCADE'))

    usuario = relationship('Usuario', back_populates='aluno')


class Funcionario(Base):
    __tablename__ = 'funcionario'

    funcionario_id = Column(Integer, primary_key=True, autoincrement=True)
    cargo = Column(String(255), nullable=False)
    setor = Column(String(255), nullable=False)
    data_admissao = Column(Date, nullable=False)


class Visitante(Base):
    __tablename__ = 'visitante'

    visitante_id = Column(Integer, primary_key=True, autoincrement=True)
    motivo_visita = Column(Text, nullable=False)
    visitado = Column(String(255), nullable=False)
    data_visita = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.user_id', ondelete='SET NULL', onupdate='CASCADE'))

    usuario = relationship('Usuario', back_populates='visitante')


def create_tables():
    engine = create_engine(DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)


def add_usuario(session, nome, sobrenome, tipo, nascimento, unidade, observacoes, permissao):
    usuario = Usuario(
        nome=nome,
        sobrenome=sobrenome,
        tipo=tipo,
        nascimento=nascimento,
        unidade=unidade,
        observacoes=observacoes,
        permissao=permissao
    )
    session.add(usuario)
    session.commit()
    return usuario


def add_aluno(session, matricula, curso, turma, usuario_id):
    aluno = Aluno(matricula=matricula, curso=curso, turma=turma, usuario_id=usuario_id)
    session.add(aluno)
    session.commit()


def add_visitante(session, motivo_visita, visitado, data_visita, usuario_id):
    visitante = Visitante(motivo_visita=motivo_visita, visitado=visitado, data_visita=data_visita,
                          usuario_id=usuario_id)
    session.add(visitante)
    session.commit()


def main():
    create_tables()

    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    usuario = add_usuario(session, 'Douglas', 'Wenzel', 'Aluno', '1990-10-15', 'Unidade A', 'Observação', True)
    add_aluno(session, '12855', 'DSM', '2024-01', usuario.user_id)

    add_visitante(session, 'Visita ao setor de TI', 'João Silva', '2024-12-02 14:30:00', usuario.user_id)

    print("Tabelas e dados criados com sucesso!")


if __name__ == '__main__':
    main()

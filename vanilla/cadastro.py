from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Pasta(Base):
    __tablename__ = 'pasta'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    caminho = Column(String(255), nullable=False)

    usuarios = relationship("Usuario", backref="pasta_associada")


# Definição da Tabela Usuario
class Usuario(Base):
    __tablename__ = 'usuario'

    user_id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    tipo = Column(String(255), nullable=False)
    nascimento = Column(Date, nullable=False)
    unidade = Column(String(255), nullable=False)
    observacoes = Column(String(255))
    permissao = Column(Boolean, nullable=False)
    pasta_id = Column(Integer, ForeignKey('pasta.id'))



DATABASE_URL = "mysql+mysqlconnector://dougl947_user:User24!e@162.241.2.230:3306/dougl947_DeltaGo"
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def cadastrar_usuario(session, nome, sobrenome, tipo, nascimento, unidade, observacoes, permissao, pasta_nome,
                      pasta_caminho):
    pasta = Pasta(nome=pasta_nome, caminho=pasta_caminho)
    session.add(pasta)
    session.commit()


    usuario = Usuario(nome=nome, sobrenome=sobrenome, tipo=tipo, nascimento=nascimento,
                      unidade=unidade, observacoes=observacoes, permissao=permissao, pasta_id=pasta.id)

    session.add(usuario)
    session.commit()
    print(f'Usuário {nome} {sobrenome} cadastrado com sucesso!')


def main():
    nome = "Douglas"
    sobrenome = "Wenzel"
    tipo = "Aluno"
    nascimento = "2000-01-01"
    unidade = "Tecnologia"
    observacoes = "Nenhuma observação"
    permissao = True
    pasta_nome = "Fotos_Douglas"
    pasta_caminho = "/caminho/para/fotos/douglas"

    cadastrar_usuario(session, nome, sobrenome, tipo, nascimento, unidade, observacoes, permissao, pasta_nome,
                      pasta_caminho)



if __name__ == "__main__":
    main()

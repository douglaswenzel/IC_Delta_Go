from pydantic import BaseModel
from datetime import date

class UsuarioResponse(BaseModel):
    user_id: int
    nome: str
    sobrenome: str
    tipo: str
    nascimento: str
    unidade: str
    observacoes: str
    permissao: bool

    class Config:
        orm_mode = True

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    user_id: int

    class Config:
        orm_mode = True

class AlunoBase(BaseModel):
    matricula: str
    curso: str
    turma: str

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    aluno_id: int

    class Config:
        orm_mode = True

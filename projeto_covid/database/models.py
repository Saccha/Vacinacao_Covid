from sqlalchemy import (
    Column, 
    Integer,
    String,
    DateTime,    
    Sequence
)
from sqlalchemy.ext.declarative import declarative_base

BancoDeDados = declarative_base()

class Cadastro(BancoDeDados):
    __tablename__ = 'cadastro'
    id = Column(Integer, Sequence('cadastro_seq'), primary_key=True)
    nome = Column(String)
    cpf = Column(Integer)
    dataNascimento = Column(DateTime)
    eProfissionalSaude = Column(String)
    dataInscricao = Column(DateTime)
    vacinado = Column(String)
    login = Column(String)
    def __init__(self, nome, cpf, dataNascimento, eProfissionalSaude, dataInscricao, vacinado, login):
        self.nome = nome
        self.cpf = cpf
        self.dataNascimento = dataNascimento
        self.eProfissionalSaude = eProfissionalSaude
        self.dataInscricao = dataInscricao
        self.vacinado = vacinado
        self.login = login

class Login(BancoDeDados):
    __tablename__ = 'login'
    id = Column(Integer, Sequence('login_seq'), primary_key=True)
    login = Column(String)
    senha = Column(String)
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha


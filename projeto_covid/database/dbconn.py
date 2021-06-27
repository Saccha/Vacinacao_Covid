import os
from database.models import BancoDeDados
from database.models import Cadastro, Login
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import update

nome_db = '../cadastrocovid19.db'
basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, nome_db))
BancoDeDados.metadata.create_all(engine) 

def obterSession():
    Session = sessionmaker(bind=engine)
    return Session()

#session.close()
#engine.dispose()

SESSENTA_ANOS = 21900

def incluirCadastro(session, 
                    nome_, 
                    cpf_, 
                    dataNascimento_, 
                    eProfissionalSaude_, 
                    dataInscricao_, 
                    vacinado_, 
                    login_):
    session.add(Cadastro(
        nome               = nome_, 
        cpf                = cpf_, 
        dataNascimento     = dataNascimento_, 
        eProfissionalSaude = eProfissionalSaude_, 
        dataInscricao      = dataInscricao_, 
        vacinado           = vacinado_, 
        login              = login_)
    )
    session.commit()
    session.close()    

def incluirLogin(session, 
                 login_, 
                 senha_):
    session.add(Login(
        login  = login_, 
        senha  = senha_)
    )
    session.commit()
    session.close()   

def profissionaisSaudeIgualMaior60(session):
    ret = session.query(Cadastro) \
    .filter(and_(Cadastro.eProfissionalSaude == 'S', 
                 Cadastro.vacinado == 'N'), 
                 func.julianday("now") - func.julianday(Cadastro.dataNascimento) >= SESSENTA_ANOS) \
    .order_by(Cadastro.dataInscricao) \
    .all()
    session.close()
    return ret

def profissionaisSaudeMenor60(session):
    ret = session.query(Cadastro) \
    .filter(and_(Cadastro.eProfissionalSaude == 'S', 
                 Cadastro.vacinado == 'N'), 
                func.julianday("now") - func.julianday(Cadastro.dataNascimento) < SESSENTA_ANOS) \
    .order_by(Cadastro.dataInscricao) \
    .all()
    session.close()
    return ret
    
def naoProfissionaisIgualMaior60(session):
    ret = session.query(Cadastro) \
    .filter(and_(Cadastro.eProfissionalSaude == 'N', Cadastro.vacinado == 'N'),
            func.julianday("now") - func.julianday(Cadastro.dataNascimento) >= SESSENTA_ANOS) \
    .order_by(Cadastro.dataInscricao) \
    .all()
    session.close()
    return ret
    
def naoProfissionaisSaudeMenor60(session):
    ret = session.query(Cadastro) \
    .filter(and_(Cadastro.eProfissionalSaude == 'N', Cadastro.vacinado == 'N'),
            func.julianday("now") - func.julianday(Cadastro.dataNascimento) < SESSENTA_ANOS) \
    .order_by(Cadastro.dataInscricao) \
    .all()
    session.close()
    return ret

def consultarLogin(session, login_, senha_):
    ret = session.query(Login) \
    .filter(and_(Login.login == login_, Login.senha == senha_)).all()
    session.close()
    return ret

def atualizarVacinado(session, login_, vacinado_):
    query = (
        update(Cadastro)
        .values(vacinado = vacinado_)
        .where(Cadastro.login == login_)
    )
    session.execute(query)
    session.commit()
    session.close()   

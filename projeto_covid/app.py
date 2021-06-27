from flask import Flask, render_template, redirect, url_for, request
from datetime import date
from datetime import datetime
from database.dbconn import obterSession
from database.dbconn import profissionaisSaudeIgualMaior60, \
                            naoProfissionaisIgualMaior60, \
                            profissionaisSaudeMenor60, \
                            naoProfissionaisSaudeMenor60, \
                            incluirCadastro, \
                            incluirLogin, \
                            consultarLogin, \
                            atualizarVacinado

nome_db = 'cadastrocovid19.db'

aplicativo = Flask(__name__)

session = obterSession()

@aplicativo.route('/')
@aplicativo.route('/index')
def index():
    return render_template('index.html', title='Welcome', 
                           profissionaisSaudeIgualMaior60=profissionaisSaudeIgualMaior60(session),
                           profissionaisSaudeMenor60=profissionaisSaudeMenor60(session),
                           naoProfissionaisIgualMaior60=naoProfissionaisIgualMaior60(session),
                           naoProfissionaisSaudeMenor60=naoProfissionaisSaudeMenor60(session))

@aplicativo.route('/registrar')
def registrar():
    return render_template('registrar.html')

@aplicativo.route('/login')
def login():
    return render_template('login.html')

@aplicativo.route('/gravar/', methods = ['POST'])
def gravar():
    if request.method == 'POST':
        # GRAVAR no banco
        form_data = request.form
        incluirCadastro(session, 
                        form_data['nome'],
                        form_data['cpf'],
                        datetime.strptime(form_data['nascimento'], '%d/%m/%Y'),
                        form_data['profissionalSaude'],
                        date.today(),
                        'N',
                        form_data['login'])
        incluirLogin(session, form_data['login'], form_data['senha1'])
        #return render_template('resposta_gravar.html', form_data = form_data)
        return redirect(url_for('index'))

@aplicativo.route('/validarLogin/', methods = ['POST'])
def validar_login():
    if request.method == 'POST':
        form_data = request.form
        if consultarLogin(session, form_data['login'], form_data['senha']):
            return render_template('resposta_login_vacinado.html',login=form_data['login'])
        return render_template('resposta_login_nok.html')

@aplicativo.route('/gravarVacinado/', methods = ['POST'])
def validar_vacinado():
    if request.method == 'POST':
        form_data = request.form
        atualizarVacinado(session, form_data['login'], form_data['vacinado'])
    return render_template('resposta_vacinado.html')

#@app.app_template_filter('to_date')
#def format_datetime(value):
#    return value.strftime('%d/%m/%Y')
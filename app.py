from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
import json

professor_name = []
professor = []
disciplina = []
turma = []
autocomplete = []
app = Flask(__name__)

def db_connect():
    conn = mysql.connector.connect(user='root', password='root',
                                   host='localhost', database='lab')
    return conn

@app.route("/" , methods=['GET', 'POST'])
def index():
    global professor, disciplina, turma, professor_name, autocomplete
    url = ''
    turmas = []
    disciplinas = []
    disciplina = ''
    turma = ''
    curso = ''
    turno = ''
    cursos = [{"acronym": "ADS", "name": "Analise e Desenvolvimento de Sistemas", "id": " "},
        {"acronym": "AU", "name": "Arquitetura e Urbanismo", "id": "13"},
        {"acronym": "CC", "name": "Ciencia da Computacao", "id": "1"},
        {"acronym": "CO", "name": "Controle de Obras", "id": ""},
        {"acronym": "EA", "name": "Engenharia Ambiental e Sanitaria", "id": "2"},
        {"acronym": "EC", "name": "Engenharia Civil", "id": "3"},
        {"acronym": "ES", "name": "Engenharia de Computacao", "id": "4"},
        {"acronym": "EO", "name": "Engenharia de Petroleo", "id": "10"},
        {"acronym": "EP", "name": "Engenharia de Producao", "id": "5"},
        {"acronym": "EE", "name": "Engenharia Eletrica", "id": "6"},
        {"acronym": "EM", "name": "Engenharia Mecanica", "id": "7"},
        {"acronym": "ER", "name": "Engenharia Mecatronica", "id": "8"},
        {"acronym": "EQ", "name": "Engenharia Quimica", "id": "11"},
        {"acronym": "GA", "name": "Gestao Ambiental", "id": ""},
        {"acronym": "PG", "name": "Petroleo e Gas", "id": ""},
        {"acronym": "RC", "name": "Redes de Computadores", "id": ""},
        {"acronym": "SI", "name": "Sistemas de Informacao", "id": "12"},
        {"acronym": "PG", "name": "Petroleo e Gas", "id": ""}, 
        ]

    if request.form.get('professor') is None:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professor")
        professor = cursor.fetchall()
        conn.close()
        autocomplete =[]
        for prof in professor:
            autocomplete.append(prof[1])

    if request.form.get('professor'):
        professor_name = request.form.get('professor')
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idprofessor FROM professor WHERE nome = '%s' " % professor_name)
        idprofessor=cursor.fetchall()
        cursor.execute("SELECT * FROM disciplina WHERE disciplina = '%s' " % idprofessor[0][0])
        disciplinas = cursor.fetchall()

    if request.form.get('professor') and request.form.get('disciplina') and request.form.get('disciplina') != 'None':
        nada = request.form.get('disciplina')
        lista = nada.split('_', 1)
        if(len(lista) > 1):
            disciplina = lista[0]
            turma = lista[1]
            nada = turma.split('-', 2)
            acronym = nada[1]
            turno = nada[2][0]
            if(turno=='M'):
                turno=1
            if(turno=='V'):
                turno=2
            if(turno=='N'):
                turno=3
            curso = filter(lambda curso:curso['acronym']==acronym,cursos)
            curso = curso[0]['id']

    return render_template('professor.html', professor=professor, disciplinas=disciplinas, turmas=turmas, autocomplete=autocomplete, disciplina=disciplina, turma=turma, professor_name=professor_name, turno=turno, curso=curso)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

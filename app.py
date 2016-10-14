from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
import json

professor_name = []
professor = []
disciplina = []
turma = []
autocomplete = []
professor_email = ''
lab_id = ''

app = Flask(__name__)

def db_connect():
    conn = mysql.connector.connect(user='root', password='root',
                                   host='localhost', database='lab')
    return conn

@app.route("/" , methods=['GET', 'POST'])
def index():
    global professor, disciplina, turma, professor_name, autocomplete, professor_email, lab_id
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
        {"acronym": "EM", "name": "Engenharia Mecanica", "id": "8"},
        {"acronym": "ER", "name": "Engenharia Mecatronica", "id": "9"},
        {"acronym": "EQ", "name": "Engenharia Quimica", "id": "11"},
        {"acronym": "GA", "name": "Gestao Ambiental", "id": ""},
        {"acronym": "PG", "name": "Petroleo e Gas", "id": ""},
        {"acronym": "RC", "name": "Redes de Computadores", "id": ""},
        {"acronym": "SI", "name": "Sistemas de Informacao", "id": "12"},
        {"acronym": "PG", "name": "Petroleo e Gas", "id": ""}, 
        ]
    if request.args.get('lab') is not None:
        lab_id = request.args.get('lab')
        
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
        idprofessor = cursor.fetchall()
        cursor.execute("SELECT * FROM disciplina WHERE disciplina = '%s' " % idprofessor[0][0])
        disciplinas = cursor.fetchall()
        cursor.execute("SELECT email FROM professor WHERE nome = '%s' " % professor_name)
        professor_email = cursor.fetchall()
    
    if request.form.get('professor') and request.form.get('disciplina') and request.form.get('disciplina') != 'None':
        select_disciplina = request.form.get('disciplina')
        disciplina = select_disciplina[:select_disciplina.index(" (")] 
        turma = select_disciplina[select_disciplina.index("(")+1:select_disciplina.index(")")]
        lista = turma.split('-', 2)
        acronym = lista[1]
        turno = lista[2][0]
        if(turno == 'M'):
            turno = 1
        if(turno == 'V'):
            turno = 2
        if(turno == 'N'):
            turno = 3
        curso = filter(lambda curso:curso['acronym'] == acronym, cursos)
        curso = curso[0]['id']

    return render_template('professor.html', professor=professor, disciplinas=disciplinas, 
        turmas=turmas, autocomplete=autocomplete, disciplina=disciplina, turma=turma, 
        professor_name=professor_name, turno=turno, curso=curso, 
        professor_email=professor_email, lab_id=lab_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

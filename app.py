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
    global professor
    global disciplina
    global turma
    global professor_name
    url = ''
    turmas = []
    disciplinas = []
    disciplina = ''
    turma = ''
    global autocomplete
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

    return render_template('professor.html', professor=professor, disciplinas=disciplinas, turmas=turmas, autocomplete=autocomplete, disciplina=disciplina, turma=turma)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

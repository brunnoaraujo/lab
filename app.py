from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

professor_name = []
professor = []
disciplina = []
turma = []

app = Flask(__name__)

def db_connect():
    conn = mysql.connector.connect(user='root', password='root',
                                   host='localhost', database='lab')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/qualquer" , methods=['GET', 'POST'])
def qualquer():
    global professor
    global disciplina
    global turma
    global professor_name
    url = ''
    turmas = []
    disciplinas = []
    autocomplete = []

    if request.form.get('professor') is None:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professor")
        professor = cursor.fetchall()
        conn.close()
        print(professor)

        for prof in professor:
            autocomplete.append(prof[1])
        print(autocomplete)

    if request.form.get('professor'):
        professor_name = request.form.get('professor')
        print(professor_name)
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idprofessor FROM professor WHERE nome = '%s' " % professor_name)
        idprofessor=cursor.fetchall()
        cursor.execute("SELECT * FROM disciplina WHERE disciplina = '%s' " % idprofessor[0][0])
        disciplinas = cursor.fetchall()

    if request.form.get('disciplina') and request.form.get('disciplina') != 'None':
        disciplina_name = request.form.get('disciplina')
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT iddisciplina FROM disciplina WHERE nome_disciplina = '%s' " % disciplina_name)
        idturma = cursor.fetchall()
        cursor.execute("SELECT * FROM turma WHERE disciplina= '%s' " % idturma[0][0])
        turmas = cursor.fetchall()

    if request.form.get('professor') and request.form.get('disciplina') and request.form.get('disciplina') != 'None'  and request.form.get('turma') and request.form.get('turma') != 'None':
        turma = request.form.get('turma')
        disciplina = request.form.get('disciplina')

        url = 'http://fs24.formsite.com/UNIFACS/form1/fill?6=1'+"&9="+str(turma)+"&13="+str(disciplina)

    return render_template('qualquer.html', professor=professor, disciplinas=disciplinas, turmas=turmas, url=url, autocomplete=autocomplete)



if __name__ == '__main__':
    app.run(debug=True)

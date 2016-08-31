from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

import mysql.connector

professor_name = None

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'very secret-y key value; shhhhh!'


def db_connect():
    conn = mysql.connector.connect(user='sql9133321', password='5l3y7xSufC',
                                   host='sql9.freemysqlhosting.net', database='sql9133321')
    return conn

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inicio')
def inicio():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professor")
    professor = cursor.fetchall()
    conn.close()
    return render_template('show-users.html', professor=professor)

@app.route("/test" , methods=['GET', 'POST'])
def test():
    global professor_name
    professor_name = request.form.get('comp_select')
    print(professor_name)

    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT idprofessor FROM professor WHERE nome = '%s' " % professor_name)
    idprofessor=cursor.fetchall()
    print(idprofessor[0][0])

    cursor.execute("SELECT * FROM disciplina WHERE disciplina = '%s' " % idprofessor[0][0])
    disciplina = cursor.fetchall()
    
    return render_template('disciplina.html', disciplina=disciplina)

@app.route("/turma" , methods=['GET', 'POST'])
def turma():
    global professor_name
    print(professor_name)
    disciplina_name = request.form.get('comp_select')
    
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT iddisciplina FROM disciplina WHERE nome_disciplina = '%s' " % disciplina_name)
    idturma = cursor.fetchall()
    print(idturma[0][0])

    cursor.execute("SELECT * FROM turma WHERE disciplina= '%s' " % idturma[0][0])
    turma = cursor.fetchall()
    return render_template('turma.html', turma=turma)


if __name__ == '__main__':
    app.run(debug=True)

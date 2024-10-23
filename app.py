from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="trabalho"
)

# Função para verificar se o usuário está logado
def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:
            flash("Por favor, faça login.")
            return redirect(url_for('login'))
    return wrap

# Rota de Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        db.commit()
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for('login'))
    return render_template('register.html')

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        usuario = cursor.fetchone()
        if usuario and check_password_hash(usuario['senha'], senha):
            session['user_id'] = usuario['id']
            return redirect(url_for('tasks'))
        else:
            flash("Email ou senha incorretos!")
    return render_template('login.html')

# Rota de Gerenciamento de Tarefas
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    user_id = session['user_id']
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        descricao = request.form['descricao']
        data_limite = request.form['data_limite']
        prioridade = request.form['prioridade']
        categoria = request.form['categoria']
        data_criacao = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            INSERT INTO tarefas (usuario_id, descricao, status, data_criacao, data_limite, prioridade, categoria)
            VALUES (%s, %s, 'Pendente', %s, %s, %s, %s)
        """, (user_id, descricao, data_criacao, data_limite, prioridade, categoria))
        db.commit()
        return redirect(url_for('tasks'))

    cursor.execute("SELECT * FROM tarefas WHERE usuario_id=%s", (user_id,))
    tarefas = cursor.fetchall()
    return render_template('tasks.html', tarefas=tarefas)

# Rota para Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

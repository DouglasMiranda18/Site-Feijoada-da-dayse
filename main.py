from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Limite: 2MB

# Criar pasta se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Banco de dados
def init_db():
    conn = sqlite3.connect('produtos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            foto TEXT,
            nome TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            valor REAL NOT NULL,
            estoque INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

def listar_produtos():
    conn = sqlite3.connect('produtos.db')
    c = conn.cursor()
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()
    
    # Converte o valor para float, tratando caso esteja vazio
    produtos_convertidos = []
    for p in produtos:
        p = list(p)
        if p[3] == '':  # Se o valor estiver vazio, define como 0.0
            p[3] = 0.0
        else:
            p[3] = float(p[3])  # Converte o valor para float
        produtos_convertidos.append(p)
    return produtos_convertidos

# Rota principal
@app.route('/')
def index():
    produtos = listar_produtos()
    return render_template('index.html', produtos=produtos, admin=False)

# Rota admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        nome = request.form['nome']
        ingredientes = request.form.get('ingredientes', '').strip()
        
        # No código do formulário admin
        valor = request.form['valor']
        if valor == '':
            valor = 0.0  # Define como 0.0 se estiver vazio
        else:
            valor = float(valor)  # Converte para float

        # Verificação para o estoque
        estoque = request.form['estoque']
        if estoque == '':
            estoque = 0  # Define como 0 se estiver vazio
        else:
            estoque = int(estoque)  # Converte para inteiro

        # Verificação para a imagem
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename != '':
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filename = None  # Caso não haja imagem, define como None
        else:
            filename = None  # Caso não haja imagem, define como None

        # Depois insira no banco
        conn = sqlite3.connect('produtos.db')
        c = conn.cursor()
        c.execute("INSERT INTO produtos (foto, nome, ingredientes, valor, estoque) VALUES (?, ?, ?, ?, ?)",
                (filename, nome, ingredientes, valor, estoque))
        conn.commit()
        conn.close()

        return redirect(url_for('admin'))

    produtos = listar_produtos()
    return render_template('admin.html', produtos=produtos, admin=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

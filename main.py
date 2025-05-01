from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Criar o banco de dados e a tabela se não existir
def init_db():
    conn = sqlite3.connect('produtos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            valor REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Página principal (exibe cardápio)
@app.route('/')
def index():
    conn = sqlite3.connect('produtos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM produtos')
    produtos = c.fetchall()
    conn.close()
    return render_template('index.html', produtos=produtos, admin=False)

# Página admin (adicionar produtos)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        nome = request.form['nome']
        ingredientes = request.form['ingredientes']
        valor = float(request.form['valor'])

        conn = sqlite3.connect('produtos.db')
        c = conn.cursor()
        c.execute('INSERT INTO produtos (nome, ingredientes, valor) VALUES (?, ?, ?)',
                  (nome, ingredientes, valor))
        conn.commit()
        conn.close()
        return redirect('/admin')

    conn = sqlite3.connect('produtos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM produtos')
    produtos = c.fetchall()
    conn.close()
    return render_template('admin.html', produtos=produtos, admin=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

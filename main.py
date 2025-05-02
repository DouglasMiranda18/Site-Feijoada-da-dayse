import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'

# ===============================
# Inicialização do Banco de Dados
# ===============================

def init_db():
    with sqlite3.connect('produtos.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                imagem TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS tamanhos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS complementos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS personalizacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                opcao TEXT NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        conn.commit()

# =========================
# Rota pública - página inicial
# =========================

@app.route('/')
def index():
    with sqlite3.connect('produtos.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM produtos')
        produtos = c.fetchall()

        produtos_completo = []
        for produto in produtos:
            produto_id = produto[0]

            c.execute('SELECT nome, preco FROM tamanhos WHERE produto_id = ?', (produto_id,))
            tamanhos = c.fetchall()

            c.execute('SELECT nome, preco FROM complementos WHERE produto_id = ?', (produto_id,))
            complementos = c.fetchall()

            c.execute('SELECT tipo, opcao FROM personalizacoes WHERE produto_id = ?', (produto_id,))
            personalizacoes = c.fetchall()

            produto_info = {
                'id': produto[0],
                'nome': produto[1],
                'descricao': produto[2],
                'imagem': produto[3],
                'tamanhos': tamanhos,
                'complementos': complementos,
                'personalizacoes': personalizacoes
            }
            produtos_completo.append(produto_info)

    return render_template('index.html', produtos=produtos_completo)

# ===============================
# Rota administrativa - /admin
# ===============================

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        # Salvar imagem
        imagem = request.files['foto']
        filename = secure_filename(imagem.filename)
        caminho_imagem = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagem.save(caminho_imagem)

        with sqlite3.connect('produtos.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO produtos (nome, descricao, imagem) VALUES (?, ?, ?)',
                      (nome, descricao, filename))
            produto_id = c.lastrowid

            # Tamanhos
            tamanho_nomes = request.form.getlist('tamanho_nome[]')
            tamanho_precos = request.form.getlist('tamanho_preco[]')
            for nome_tam, preco in zip(tamanho_nomes, tamanho_precos):
                c.execute('INSERT INTO tamanhos (produto_id, nome, preco) VALUES (?, ?, ?)',
                          (produto_id, nome_tam, preco))

            # Complementos
            complemento_nomes = request.form.getlist('complemento_nome[]')
            complemento_precos = request.form.getlist('complemento_preco[]')
            for nome_comp, preco in zip(complemento_nomes, complemento_precos):
                if nome_comp.strip():
                    c.execute('INSERT INTO complementos (produto_id, nome, preco) VALUES (?, ?, ?)',
                              (produto_id, nome_comp, preco))

            # Personalizações
            tipos = request.form.getlist('personalizacao_tipo[]')
            opcoes = request.form.getlist('personalizacao_opcao[]')
            for tipo, opcao in zip(tipos, opcoes):
                if tipo.strip() and opcao.strip():
                    c.execute('INSERT INTO personalizacoes (produto_id, tipo, opcao) VALUES (?, ?, ?)',
                              (produto_id, tipo, opcao))

            conn.commit()

        return redirect(url_for('admin'))

    with sqlite3.connect('produtos.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM produtos')
        produtos = c.fetchall()
        produtos = [{'id': p[0], 'nome': p[1], 'descricao': p[2], 'imagem': p[3]} for p in produtos]

    return render_template('admin.html', produtos=produtos)

@app.route('/admin/excluir/<int:id>')
def excluir_produto(id):
    with sqlite3.connect('produtos.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM tamanhos WHERE produto_id = ?', (id,))
        c.execute('DELETE FROM complementos WHERE produto_id = ?', (id,))
        c.execute('DELETE FROM personalizacoes WHERE produto_id = ?', (id,))
        c.execute('DELETE FROM produtos WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('admin'))

@app.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    with sqlite3.connect('produtos.db') as conn:
        c = conn.cursor()
        if request.method == 'POST':
            nome = request.form['nome']
            descricao = request.form['descricao']

            c.execute('UPDATE produtos SET nome = ?, descricao = ? WHERE id = ?', (nome, descricao, id))
            conn.commit()
            return redirect(url_for('admin'))

        c.execute('SELECT * FROM produtos WHERE id = ?', (id,))
        produto = c.fetchone()

    if produto:
        produto_dict = {'id': produto[0], 'nome': produto[1], 'descricao': produto[2]}
        return render_template('editar.html', produto=produto_dict)
    return redirect(url_for('admin'))


# ===========================
# Inicialização da Aplicação
# ===========================

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

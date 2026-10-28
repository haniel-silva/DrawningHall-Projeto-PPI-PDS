from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'

# Função para conectar diretamente ao banco de dados no MySQL Workbench
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="labinfo",       # Substitua pela sua senha do MySQL Workbench
        database="drawninghall_db"   # Certifique-se de criar este banco antes no Workbench
    )

@app.route("/")
def index():
    if 'usuario' in session:
        return redirect(url_for('definicao'))
    return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
    acao = request.form.get('acao')
    nome = request.form.get('usuario')
    senha = request.form.get('senha')
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    if acao == 'cadastrar':
        # Verifica se o usuário já existe
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
        usuario_existente = cursor.fetchone()
        
        if usuario_existente:
            cursor.close()
            conexao.close()
            return render_template('index.html', erro="Este nome de usuário já está em uso!")
        
        # COMANDO CRUD (CREATE) em SQL puro
        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (nome, senha))
        conexao.commit()
        
        cursor.close()
        conexao.close()
        
        session['usuario'] = nome
        return redirect(url_for('definicao'))
        
    elif acao == 'entrar':
        # COMANDO CRUD (READ) em SQL puro para validar o login
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (nome, senha))
        usuario = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        
        if usuario:
            session['usuario'] = nome
            return redirect(url_for('definicao'))
        return render_template('index.html', erro="Usuário ou senha incorretos!")

@app.route("/logout")
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route("/setup")
def definicao():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('setup.html')

@app.route("/desenho", methods=["POST"])
def desenhar():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    altura = request.form.get('altura-escolher', 600)
    largura = request.form.get('largura-escolher', 800)
    return render_template('desenho.html', altura=altura, largura=largura)

@app.route("/salvar-mural", methods=["POST"])
def salvar_mural():
    if 'usuario' not in session:
        return redirect(url_for('index'))
        
    dados_imagem = request.form.get('imagem_base64')
    titulo = request.form.get('titulo_desenho', 'Minha Arte')
    autor = session['usuario']
    
    if dados_imagem:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        
        # COMANDO CRUD (CREATE) em SQL puro para salvar o desenho e a imagem em Base64
        cursor.execute(
            "INSERT INTO desenhos (titulo, autor, imagem) VALUES (%s, %s, %s)",
            (titulo, autor, dados_imagem)
        )
        conexao.commit()
        
        cursor.close()
        conexao.close()
        
    return redirect(url_for('ver_mural'))

@app.route("/mural")
def ver_mural():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    # COMANDO CRUD (READ) em SQL puro para listar todos os desenhos do mais recente para o mais antigo
    cursor.execute("SELECT id, titulo, autor, imagem FROM desenhos ORDER BY id DESC")
    desenhos_db = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return render_template('mural.html', desenhos=desenhos_db, usuario_atual=session.get('usuario'))

@app.route("/excluir/<int:id_desenho>", methods=["POST"])
def excluir(id_desenho):
    if 'usuario' not in session:
        return redirect(url_for('index'))
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    # Verifica se o desenho pertence ao usuário logado antes de excluir
    cursor.execute("SELECT autor FROM desenhos WHERE id = %s", (id_desenho,))
    desenho = cursor.fetchone()
    
    if desenho and desenho['autor'] == session['usuario']:
        # COMANDO CRUD (DELETE) em SQL puro
        cursor.execute("DELETE FROM desenhos WHERE id = %s", (id_desen_desenho := id_desenho)) # ou simplesmente id_desenho
        cursor.execute("DELETE FROM desenhos WHERE id = %s", (id_desenho,))
        conexao.commit()
        
    cursor.close()
    conexao.close()
    
    return redirect(url_for('ver_mural'))

if __name__ == "__main__":
    app.run(debug=True)
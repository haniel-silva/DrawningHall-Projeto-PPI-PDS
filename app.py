from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chavesecreta123'

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="labinfo",       
        database="drawninghall_db"   
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
      
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
        usuario_existente = cursor.fetchone()
        
        if usuario_existente:
            cursor.close()
            conexao.close()
            return render_template('index.html', erro="Este nome de usuário já está em uso!")
        
      
        cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (nome, senha))
        conexao.commit()
        
        cursor.close()
        conexao.close()
        
        session['usuario'] = nome
        return redirect(url_for('definicao'))
        
    elif acao == 'entrar':
 
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
    
    cursor.execute("SELECT autor FROM desenhos WHERE id = %s", (id_desenho,))
    desenho = cursor.fetchone()
    
    if desenho and desenho['autor'] == session['usuario']:
        # Corrigido: passando apenas a tupla limpa com o ID
        cursor.execute("DELETE FROM desenhos WHERE id = %s", (id_desenho,))
        conexao.commit()
        
    cursor.close()
    conexao.close()
    
    return redirect(url_for('ver_mural'))

if __name__ == "__main__":
    app.run(debug=True)
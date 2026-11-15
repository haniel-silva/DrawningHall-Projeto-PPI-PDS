from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuração robusta: lê do arquivo config.py ou pega variáveis de ambiente (ideal para o Vercel/Supabase)
app.config.from_object('config')
app.secret_key = os.environ.get('SECRET_KEY', 'chavesecreta123')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importa os models para o SQLAlchemy reconhecer as tabelas
from models import Usuario, Desenho

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

    
    if acao == 'cadastrar':
        usuario_existente = Usuario.query.filter_by(nome=nome).first()
        
        if usuario_existente:
            return render_template('index.html', erro="Este nome de usuário já está em uso!")
        
        novo_usuario = Usuario(nome=nome, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        
        session['usuario'] = nome
        return redirect(url_for('definicao'))
        
    elif acao == 'entrar':
        usuario = Usuario.query.filter_by(nome=nome, senha=senha).first()
        
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
        novo_desenho = Desenho(titulo=titulo, autor=autor, imagem=dados_imagem)
        db.session.add(novo_desenho)
        db.session.commit()
        
    return redirect(url_for('ver_mural'))

@app.route("/mural")
def ver_mural():
    # Busca os desenhos ordenados do mais recente para o mais antigo
    desenhos_db = Desenho.query.order_by(Desenho.id.desc()).all()
    return render_template('mural.html', desenhos=desenhos_db, usuario_atual=session.get('usuario'))

@app.route("/excluir/<int:id_desenho>", methods=["POST"])
def excluir(id_desenho):
    if 'usuario' not in session:
        return redirect(url_for('index'))
    
    desenho = Desenho.query.get(id_desenho)
    
    if desenho and desenho.autor == session['usuario']:
        db.session.delete(desenho)
        db.session.commit()
        
    return redirect(url_for('ver_mural'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)

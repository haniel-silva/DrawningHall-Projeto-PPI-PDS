from app import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

class Desenho(db.Model):
    __tablename__ = 'desenhos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False, default='Minha Arte')
    autor = db.Column(db.String(80), nullable=False)
    imagem = db.Column(db.Text, nullable=False) 
    
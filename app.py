from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/setup")
def definicao():
    return render_template('setup.html')

@app.route("/desenho", methods=["POST"])
def desenhar():
    altura = request.form.get('altura-escolher', 400)
    largura = request.form.get('largura-escolher', 400)
    return render_template('desenho.html', altura=altura, largura=largura)

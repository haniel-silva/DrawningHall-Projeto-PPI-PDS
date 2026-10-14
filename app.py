from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/setup")
def definicao():
    print('oi')
    return render_template('setup.html')

@app.route("/desenho")
def desenhar():
    return render_template('desenho.html')

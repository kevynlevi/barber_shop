from flask import Flask, render_template
from blueprints.login import login
from flask_sqlalchemy import SQLAlchemy
from config import Config
from modals.modal import db, Usuario, Cliente, Funcionario, Servico, Agendamento, HorarioDisponivel, Pagamento
import os

app = Flask(__name__)
app.register_blueprint(login)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_salao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.urandom(24)

db.init_app(app)  # Inicializa o SQLAlchemy com a app Flask

@app.route("/")
def inicio():
    return render_template("index.html")

# Cria as tabelas no banco de dados antes de iniciar o servidor
with app.app_context():
    db.create_all()

# Executa o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)

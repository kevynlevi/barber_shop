from flask import Blueprint, render_template, request, flash, redirect
from modals.modal import Usuario, Cliente, Funcionario, Servico, Agendamento, HorarioDisponivel, Pagamento

# Definindo o blueprint
login = Blueprint('login_page', __name__, template_folder='templates')

# Rota de login
@login.route("/login", methods=['POST', 'GET'])
def login_page():
    return render_template("login.html")

# Rota de registro
@login.route("/registro", methods=['POST', 'GET'])
def registro():
    return render_template("registro.html")

@login.route("/cadastro", methods=['POST'])
def cadastro():
    from run import db  # Importação local para evitar circularidade
    
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    cpf = request.form.get("cpf")
    tipo= "cliente"
    
    
    usuario_email = Usuario.query.filter_by(email=email).first()
    usuario_cpf = Usuario.query.filter_by(cpf=cpf).first()
    
    if usuario_email:
        flash("Este email já está cadastrado. Tente novamente.")
        return redirect("/registro")
    
    if usuario_cpf:
        flash("Este CPF já está cadastrado.")
        return redirect("/registro")
    
    novo_usuario = Usuario(nome=nome, email=email, cpf=cpf)
    novo_usuario.set_senha(senha)
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    flash("Usuário cadastrado com sucesso!")
    return redirect("/")  # Redireciona para a página inicial após o cadastro

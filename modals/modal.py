from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Tabela de Usuários
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Novo campo para nome
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)  # Novo campo para CPF
    tipo = db.Column(db.Enum('Administrador', 'Funcionário', 'Cliente'), default='Cliente', nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

# Tabela de Clientes
class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

# Tabela de Funcionários
class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    especialidade = db.Column(db.String(100))  # Ex: Barbeiro, Cabeleireiro, etc.
    data_contratacao = db.Column(db.Date)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

# Tabela de Serviços
class Servico(db.Model):
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao = db.Column(db.Time, nullable=False)  # Duração do serviço
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

# Tabela de Agendamentos
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    data_agendamento = db.Column(db.Date, nullable=False)
    hora_agendamento = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum('Pendente', 'Concluído', 'Cancelado'), default='Pendente')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship('Cliente', backref='agendamentos')
    funcionario = db.relationship('Funcionario', backref='agendamentos')
    servico = db.relationship('Servico', backref='agendamentos')

# Tabela de Horários Disponíveis para Funcionários
class HorarioDisponivel(db.Model):
    __tablename__ = 'horarios_disponiveis'
    
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    dia_semana = db.Column(db.Enum('Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)

    funcionario = db.relationship('Funcionario', backref='horarios_disponiveis')

# Tabela de Pagamentos
class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    agendamento_id = db.Column(db.Integer, db.ForeignKey('agendamentos.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    metodo_pagamento = db.Column(db.Enum('Dinheiro', 'Cartão', 'Pix'), nullable=False)
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)

    agendamento = db.relationship('Agendamento', backref='pagamentos')

from src.controllers.agendamentos.cadastrar_agendamento import cadastrar_agendamento
from src.controllers.agendamentos.listar_agendamentos import listar_agendamentos
from flask import Blueprint

# Criacao da instancia do Blueprint de agendamentos
agendamentos_bp = Blueprint('agendamentos', __name__)

# Rota de listagem de agendamentos
agendamentos_bp.route('/listar', methods=['GET'])(listar_agendamentos)

# Rota de cadastro de agendamentos
agendamentos_bp.route('/cadastrar', methods=['POST'])(cadastrar_agendamento)
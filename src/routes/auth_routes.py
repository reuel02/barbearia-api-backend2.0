from src.controllers.auth.login import login
from src.controllers.auth.cadastro import cadastrar
from flask import Blueprint

# Criacao da instancia do Blueprint de autenticacao
auth_bp = Blueprint('auth', __name__)

# Rota de cadastro
auth_bp.route('/cadastrar', methods=['POST'])(cadastrar)

# Rota de login
auth_bp.route('/login', methods=['POST'])(login)
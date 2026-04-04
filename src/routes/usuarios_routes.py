from src.controllers.usuarios.listar_usuarios_por_role import listar_usuarios_por_role
from src.controllers.usuarios.cadastrar_funcionario import cadastrar_funcionario
from src.controllers.usuarios.cadastrar_cliente import cadastrar_cliente
from flask import Blueprint

# Criacao da instancia do Blueprint de autenticacao
usuarios_bp = Blueprint("usuarios", __name__)

# Rota de cadastro de clientes
usuarios_bp.route("/cadastrar/cliente/<empresa_id>", methods=["POST"])(
    cadastrar_cliente
)

# Rota de cadastro de funcionarios
usuarios_bp.route("/cadastrar/funcionario", methods=["POST"])(cadastrar_funcionario)

# Rota de listagem de usuarios
usuarios_bp.route("/listar/<role>", methods=["GET"])(listar_usuarios_por_role)

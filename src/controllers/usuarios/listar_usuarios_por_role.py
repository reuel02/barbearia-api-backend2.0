from flask_jwt_extended.utils import get_jwt
from src.middlewares.admin_required import admin_required
from flask import jsonify
from src.schemas.usuario_schema import UsuarioSchema
from src.models import Usuario


# Controlador de listagem de usuarios por Role = CLIENTE OU ADMIN OU STAFF
@admin_required()
def listar_usuarios_por_role(role):
    try:
        schema = UsuarioSchema(many=True)

        token_decodificado = get_jwt()

        empresa_id_token = token_decodificado["empresa_id"]

        resultado = Usuario.query.filter_by(
            role=role, empresa_id=empresa_id_token
        ).all()

        dados = schema.dump(resultado)

        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500

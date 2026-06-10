from flask import jsonify
from src.schemas.usuario_schema import UsuarioSchema
from src.models import Usuario
from src.models.usuario import RoleUsuario


def listar_barbeiros_publica(empresa_id):
    try:
        schema = UsuarioSchema(many=True)
        resultado = Usuario.query.filter_by(
            role=RoleUsuario.FUNCIONARIO, empresa_id=empresa_id
        ).all()
        dados = schema.dump(resultado)
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado", "erro": str(e)}), 500

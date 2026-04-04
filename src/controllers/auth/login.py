from werkzeug.security import check_password_hash
from src.models import Usuario
from src.schemas.login_schema import LoginSchema
from flask import request, jsonify
from flask_jwt_extended import create_access_token


# Controlador de login de ADMIN
def login():
    try:
        schema = LoginSchema()
        dados = schema.load(request.json)

        resultado = Usuario.query.filter_by(email=dados["email"]).first()

        if resultado is None:
            return jsonify({"mensagem": "Email incorreto"}), 401

        senha_valida = check_password_hash(resultado.senha_hash, dados["senha"])

        if not senha_valida:
            return jsonify({"mensagem": "Senha incorreta"}), 401

        token = create_access_token(
            identity=str(resultado.id),
            additional_claims={
                "empresa_id": str(resultado.empresa_id),
                "role": resultado.role.value,
            },
        )

        return jsonify({"mensagem": "Usuario logado com sucesso", "token": token}), 200

    except Exception as e:
        print(e)
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500

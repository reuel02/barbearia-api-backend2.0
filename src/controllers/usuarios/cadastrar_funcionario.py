from src.middlewares.admin_required import admin_required
from werkzeug.security import generate_password_hash
from flask import request, jsonify
from flask_jwt_extended import get_jwt
from src.schemas.usuario_schema import UsuarioSchema
from src.models import Usuario
from db import db

@admin_required()
def cadastrar_funcionario():
    try:
        schema = UsuarioSchema()

        dados = schema.load(request.json)

        senha_hash = generate_password_hash(dados["senha"])

        token_decodificado = get_jwt()

        empresa_id_token = token_decodificado["empresa_id"]

        usuario = Usuario(
            empresa_id = empresa_id_token,
            nome = dados["nome"],
            email = dados["email"],
            senha_hash = senha_hash,
            role = "STAFF",
            telefone = dados.get("telefone")
        )

        db.session.add(usuario)
        db.session.commit()

        return jsonify({"mensagem": "Usuario cadastrado com sucesso."}), 201

    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500
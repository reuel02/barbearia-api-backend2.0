from werkzeug.security import generate_password_hash
from flask import request, jsonify
from src.schemas.usuario_schema import UsuarioSchema
from src.models import Usuario
from db import db


# Controlador de cadastro de clientes
def cadastrar_cliente(empresa_id):
    try:
        schema = UsuarioSchema()

        dados = schema.load(request.json)

        senha_hash = generate_password_hash(dados["senha"])

        usuario = Usuario(
            empresa_id=empresa_id,
            nome=dados["nome"],
            email=dados["email"],
            senha_hash=senha_hash,
            role="CLIENTE",
            telefone=dados.get("telefone"),
        )

        db.session.add(usuario)
        db.session.commit()

        return jsonify({"mensagem": "Usuario cadastrado com sucesso."}), 201

    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500

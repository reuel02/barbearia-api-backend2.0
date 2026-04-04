from src.middlewares.admin_required import admin_required
from src.schemas.servico_schema import ServicoSchema
from src.models import Servico
from flask import request, jsonify
from db import db
from flask_jwt_extended import get_jwt


# Controlador de cadastro de servicos
@admin_required()
def cadastrar_servico():
    try:
        schema = ServicoSchema()

        dados = schema.load(request.json)

        token_decodificado = get_jwt()

        empresa_id_token = token_decodificado["empresa_id"]

        servico = Servico(
            empresa_id=empresa_id_token,
            nome=dados["nome"],
            preco=dados["preco"],
            duracao=dados["duracao"],
        )

        db.session.add(servico)
        db.session.commit()

        return jsonify({"mensagem": "Servico cadastrado com sucesso"}), 201

    except Exception as e:
        print(e)
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500

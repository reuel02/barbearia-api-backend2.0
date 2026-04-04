from flask import jsonify, request
from flask_jwt_extended.utils import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from src.schemas.agendamento_schema import AgendamentoSchema
from src.models.agendamento import StatusAgendamento
from src.models import Agendamento
from db import db


@jwt_required()
def atualizar_status_agendamento(agendamento_id):
    try:
        novo_status_req = request.json.get("status")

        if not novo_status_req:
            return jsonify({"erro": "Envie o 'status'."}), 400

        try:
            status_enum = StatusAgendamento[novo_status_req]
        except KeyError:
            return jsonify({"erro": "Status inválido."}), 400

        agendamento = Agendamento.query.get(agendamento_id)

        if not agendamento:
            return jsonify({"erro": "Agendamento não encontrado!"}), 404

        agendamento.status = status_enum
        db.session.commit()

        return jsonify({"mensagem": "Status atualizado com sucesso."}), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500

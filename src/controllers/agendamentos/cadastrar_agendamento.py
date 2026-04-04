from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended.utils import get_jwt
from flask import request, jsonify
from src.schemas.agendamento_schema import AgendamentoSchema
from src.models import Agendamento, Empresa
from src.models.agendamento import StatusAgendamento
from datetime import time
from db import db

@jwt_required()
def cadastrar_agendamento():
    try:
        token = get_jwt()

        schema = AgendamentoSchema()

        dados = schema.load(request.json)

        empresa = Empresa.query.get(token["empresa_id"])
        hora_desejada = dados["data_hora"].time()
        
        abertura = empresa.hora_abertura or time(8, 0)
        fechamento = empresa.hora_fechamento or time(18, 0)
        
        if hora_desejada < abertura or hora_desejada >= fechamento:
            return jsonify({
                "mensagem": f"Horario invalido. A barbearia funciona das {abertura.strftime('%H:%M')} as {fechamento.strftime('%H:%M')}"
            }), 400

        consulta = Agendamento.query.filter_by(barbeiro_id=dados["barbeiro_id"], data_hora=dados["data_hora"], status=StatusAgendamento.PENDENTE).first()

        if consulta:
            return jsonify({"mensagem": "Ja existe um agendamento feito nesse mesmo dia e horario"}), 400
        
        agendamento = Agendamento(
            empresa_id = token["empresa_id"],
            cliente_id = token["sub"],
            barbeiro_id = dados["barbeiro_id"],
            servico_id = dados["servico_id"],
            data_hora = dados["data_hora"]
        )

        db.session.add(agendamento)
        db.session.commit()

        return jsonify({"mensagem": "Agendamento realizado com sucesso", "agendamento": schema.dump(agendamento)}), 201

    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500


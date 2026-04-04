from src.schemas.agendamento_schema import AgendamentoSchema
from src.models import Agendamento
from flask_jwt_extended.utils import get_jwt
from src.middlewares.admin_required import admin_required
from flask import jsonify, request
from sqlalchemy import func


# Controlador de listagem de agendamentos
@admin_required()
def listar_agendamentos():
    try:
        token = get_jwt()

        empresa_id = token["empresa_id"]

        schema = AgendamentoSchema(many=True)

        query = Agendamento.query.filter_by(empresa_id=empresa_id)

        filtro_status = request.args.get("status")
        filtro_barbeiro = request.args.get("barbeiro_id")
        filtro_data = request.args.get("data")

        if filtro_status:
            query = query.filter_by(status=filtro_status)

        if filtro_barbeiro:
            query = query.filter_by(barbeiro_id=filtro_barbeiro)

        if filtro_data:
            query = query.filter(func.date(Agendamento.data_hora) == filtro_data)

        resultado = query.all()

        if not resultado:
            return jsonify({"mensagem": "Nenhum agendamento encontrado."}), 404

        dados = schema.dump(resultado)

        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500

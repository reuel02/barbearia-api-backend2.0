from src.schemas.servico_schema import ServicoSchema
from src.models import Servico
from flask import jsonify


# Controlador de listagem de servicos
def listar_servicos(empresa_id):
    try:
        schema = ServicoSchema(many=True)

        resultado = Servico.query.filter_by(empresa_id=empresa_id).all()

        dados = schema.dump(resultado)

        return jsonify(dados), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500

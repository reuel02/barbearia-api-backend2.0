from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.models.agendamento import Agendamento
from src.models.usuario import Usuario


class AgendamentoSchema(SQLAlchemyAutoSchema):
    cliente_nome = fields.Method("get_cliente_nome")
    barbeiro_nome = fields.Method("get_barbeiro_nome")

    class Meta:
        model = Agendamento
        include_fk = True
        load_instance = False
        dump_only = ("id", "empresa_id", "status", "cliente_id")

    def get_cliente_nome(self, obj):
        cliente = Usuario.query.get(obj.cliente_id)
        return cliente.nome if cliente else "Desconhecido"

    def get_barbeiro_nome(self, obj):
        barbeiro = Usuario.query.get(obj.barbeiro_id)
        return barbeiro.nome if barbeiro else "Desconhecido"

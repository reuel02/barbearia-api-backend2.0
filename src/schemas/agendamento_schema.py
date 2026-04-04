from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.models.agendamento import Agendamento


class AgendamentoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Agendamento
        include_fk = True
        load_instance = False
        dump_only = ("id", "empresa_id", "status", "cliente_id")

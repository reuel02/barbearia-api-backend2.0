from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models.servico import Servico


class ServicoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Servico
        load_instance = False
        dump_only = ("id", "empresa_id", "ativo")

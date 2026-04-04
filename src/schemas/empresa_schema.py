from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models.empresa import Empresa


class EmpresaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empresa  # A classe do seu modelo
        load_instance = True  # Isso ajuda na hora de receber POST e salvar no banco

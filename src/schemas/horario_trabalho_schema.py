from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models.horario_trabalho import HorarioTrabalho


class HorarioTrabalhoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HorarioTrabalho
        load_instance = True

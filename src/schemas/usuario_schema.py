from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.models.usuario import Usuario

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario 
        load_instance = False 
        dump_only = ("id", "empresa_id", "ativo") 
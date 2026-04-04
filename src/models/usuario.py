import uuid
import enum
from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON


# Configurando as opções do Enum
class RoleUsuario(enum.Enum):
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"
    CLIENTE = "CLIENTE"


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("empresas.id"), nullable=False
    )
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleUsuario), nullable=False)
    telefone = db.Column(db.String(20))

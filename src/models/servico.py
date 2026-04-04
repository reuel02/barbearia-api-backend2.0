import uuid
from db import db
from sqlalchemy.dialects.postgresql import UUID


class Servico(db.Model):
    __tablename__ = "servicos"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("empresas.id"), nullable=False
    )
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # Tempo em minutos
    ativo = db.Column(db.Boolean, default=True)

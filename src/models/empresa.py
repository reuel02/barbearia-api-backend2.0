import uuid
from datetime import datetime, time
from db import db
from sqlalchemy.dialects.postgresql import UUID, JSON


class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    cnpj = db.Column(
        db.String(14), nullable=True
    )  # nullable=True permite cadastro sem CNPJ inicial
    hora_abertura = db.Column(db.Time, default=time(8, 0))
    hora_fechamento = db.Column(db.Time, default=time(18, 0))
    configuracoes = db.Column(JSON, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

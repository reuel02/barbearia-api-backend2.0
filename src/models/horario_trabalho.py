import uuid
from db import db
from sqlalchemy.dialects.postgresql import UUID


class HorarioTrabalho(db.Model):
    __tablename__ = "horarios_trabalho"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False
    )
    dia_semana = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)

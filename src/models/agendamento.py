import uuid
import enum
from db import db
from sqlalchemy.dialects.postgresql import UUID

class StatusAgendamento(enum.Enum):
    PENDENTE = 'PENDENTE'
    CONFIRMADO = 'CONFIRMADO'
    CONCLUIDO = 'CONCLUIDO'
    CANCELADO = 'CANCELADO'

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = db.Column(UUID(as_uuid=True), db.ForeignKey('empresas.id'), nullable=False)
    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'), nullable=False)
    barbeiro_id = db.Column(UUID(as_uuid=True), db.ForeignKey('usuarios.id'), nullable=False)
    servico_id = db.Column(UUID(as_uuid=True), db.ForeignKey('servicos.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(StatusAgendamento), default=StatusAgendamento.PENDENTE)

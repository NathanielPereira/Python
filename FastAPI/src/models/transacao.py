from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.sql import func

from src.database import metadata

transacoes = Table(
    "transacoes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("conta_id", Integer, ForeignKey("contas.id"), nullable=False, index=True),
    Column("tipo", String(10), nullable=False),  # 'deposito' ou 'saque'
    Column("valor", Float, nullable=False),
    Column("descricao", String(255)),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)


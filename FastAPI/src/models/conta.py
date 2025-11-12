from sqlalchemy import Column, Float, Integer, String, Table

from src.database import metadata

contas = Table(
    "contas",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("numero", String(20), unique=True, nullable=False, index=True),
    Column("titular", String(100), nullable=False),
    Column("saldo", Float, nullable=False, default=0.0),
)


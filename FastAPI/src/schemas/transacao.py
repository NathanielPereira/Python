from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class TipoTransacao(str, Enum):
    """Enum para tipos de transação"""
    DEPOSITO = "deposito"
    SAQUE = "saque"


class TransacaoIn(BaseModel):
    """Schema para criação de transação"""
    tipo: TipoTransacao = Field(..., description="Tipo da transação: 'deposito' ou 'saque'")
    valor: float = Field(..., gt=0, description="Valor da transação (deve ser maior que zero)")
    descricao: str | None = Field(None, description="Descrição opcional da transação", max_length=255)

    @field_validator("valor")
    @classmethod
    def validate_valor(cls, v):
        if v <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return v


class TransacaoOut(BaseModel):
    """Schema para resposta de transação"""
    id: int
    conta_id: int
    tipo: str
    valor: float
    descricao: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ContaExtrato(BaseModel):
    """Schema para conta no extrato"""
    id: int
    numero: str
    titular: str


class ExtratoOut(BaseModel):
    """Schema para resposta de extrato bancário"""
    conta: ContaExtrato
    transacoes: list[TransacaoOut]
    saldo_atual: float


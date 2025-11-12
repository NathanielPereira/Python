from pydantic import BaseModel, Field


class ContaIn(BaseModel):
    """Schema para criação de conta corrente"""
    numero: str = Field(..., description="Número da conta corrente", max_length=20)
    titular: str = Field(..., description="Nome do titular da conta", max_length=100)


class ContaOut(BaseModel):
    """Schema para resposta de conta corrente"""
    id: int
    numero: str
    titular: str
    saldo: float

    class Config:
        from_attributes = True


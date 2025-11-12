from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    """Schema para requisição de login"""
    user_id: int = Field(..., description="ID do usuário para autenticação", gt=0)
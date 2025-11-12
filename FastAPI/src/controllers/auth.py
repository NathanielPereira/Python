from fastapi import APIRouter

from src.schemas.auth import LoginIn
from src.security import sign_jwt
from src.views.auth import LoginOut

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/login",
    response_model=LoginOut,
    summary="Autenticar usuário",
    description="Realiza a autenticação do usuário e retorna um token JWT para acesso aos endpoints protegidos",
)
async def login(data: LoginIn):
    """Endpoint para autenticação e obtenção de token JWT"""
    return sign_jwt(user_id=data.user_id)
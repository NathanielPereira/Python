from fastapi import APIRouter, Depends, status

from src.schemas.conta import ContaIn, ContaOut
from src.security import login_required
from src.services.conta import ContaService

router = APIRouter(prefix="/contas", tags=["Contas"])

service = ContaService()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ContaOut,
    summary="Criar nova conta corrente",
    description="Cria uma nova conta corrente com saldo inicial zero",
)
async def create_conta(conta: ContaIn, user_id: int = Depends(login_required)):
    """Endpoint para criar uma nova conta corrente"""
    conta_id = await service.create(conta)
    conta_criada = await service.get_by_id(conta_id)
    return ContaOut(**dict(conta_criada))


@router.get(
    "/{conta_id}",
    response_model=ContaOut,
    summary="Buscar conta por ID",
    description="Retorna os dados de uma conta corrente específica",
)
async def get_conta(conta_id: int, user_id: int = Depends(login_required)):
    """Endpoint para buscar uma conta por ID"""
    conta = await service.get_by_id(conta_id)
    return ContaOut(**dict(conta))


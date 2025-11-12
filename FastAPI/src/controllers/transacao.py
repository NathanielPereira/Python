from fastapi import APIRouter, Depends, status

from src.schemas.transacao import ContaExtrato, ExtratoOut, TransacaoIn, TransacaoOut
from src.security import login_required
from src.services.conta import ContaService
from src.services.transacao import TransacaoService

router = APIRouter(prefix="/transacoes", tags=["Transações"])

transacao_service = TransacaoService()
conta_service = ContaService()


@router.post(
    "/contas/{conta_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=TransacaoOut,
    summary="Criar transação bancária",
    description="Cria uma nova transação (depósito ou saque) para uma conta corrente. "
    "Valida se o valor é positivo e se há saldo suficiente para saques.",
)
async def create_transacao(
    conta_id: int,
    transacao: TransacaoIn,
    user_id: int = Depends(login_required),
):
    """Endpoint para criar uma transação (depósito ou saque)"""
    transacao_criada = await transacao_service.create(conta_id, transacao)
    return TransacaoOut(**dict(transacao_criada))


@router.get(
    "/contas/{conta_id}/extrato",
    response_model=ExtratoOut,
    summary="Obter extrato bancário",
    description="Retorna o extrato completo de uma conta corrente, incluindo todas as transações realizadas e o saldo atual",
)
async def get_extrato(conta_id: int, user_id: int = Depends(login_required)):
    """Endpoint para obter o extrato de uma conta"""
    # Busca a conta
    conta = await conta_service.get_by_id(conta_id)

    # Busca todas as transações
    transacoes_list = await transacao_service.get_by_conta(conta_id)

    # Formata a resposta
    return ExtratoOut(
        conta=ContaExtrato(
            id=conta.id,
            numero=conta.numero,
            titular=conta.titular,
        ),
        transacoes=[TransacaoOut(**dict(trans)) for trans in transacoes_list],
        saldo_atual=float(conta.saldo),
    )


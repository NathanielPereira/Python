from databases.interfaces import Record

from src.database import database
from src.exceptions import InsufficientBalanceError, InvalidAmountError, NotFoundContaError, NotFoundTransacaoError
from src.models.transacao import transacoes
from src.schemas.transacao import TipoTransacao, TransacaoIn
from src.services.conta import ContaService


class TransacaoService:
    def __init__(self):
        self.conta_service = ContaService()

    async def create(self, conta_id: int, transacao: TransacaoIn) -> Record:
        """Cria uma nova transação (depósito ou saque)"""
        # Valida se a conta existe
        conta = await self.conta_service.get_by_id(conta_id)

        # Calcula novo saldo
        saldo_atual = float(conta.saldo)

        if transacao.tipo == TipoTransacao.SAQUE:
            # Valida saldo suficiente para saque
            if saldo_atual < transacao.valor:
                raise InsufficientBalanceError
            novo_saldo = saldo_atual - transacao.valor
        else:  # DEPOSITO
            novo_saldo = saldo_atual + transacao.valor

        # Atualiza saldo da conta
        await self.conta_service.update_saldo(conta_id, novo_saldo)

        # Cria a transação
        command = transacoes.insert().values(
            conta_id=conta_id,
            tipo=transacao.tipo.value,
            valor=transacao.valor,
            descricao=transacao.descricao,
        )
        transacao_id = await database.execute(command)

        # Retorna a transação criada
        return await self.get_by_id(transacao_id)

    async def get_by_id(self, transacao_id: int) -> Record:
        """Busca uma transação por ID"""
        query = transacoes.select().where(transacoes.c.id == transacao_id)
        transacao = await database.fetch_one(query)
        if not transacao:
            raise NotFoundTransacaoError
        return transacao

    async def get_by_conta(self, conta_id: int) -> list[Record]:
        """Busca todas as transações de uma conta"""
        # Valida se a conta existe
        await self.conta_service.get_by_id(conta_id)

        query = transacoes.select().where(transacoes.c.conta_id == conta_id).order_by(transacoes.c.created_at.desc())
        return await database.fetch_all(query)


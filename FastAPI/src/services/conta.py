from databases.interfaces import Record

from src.database import database
from src.exceptions import NotFoundContaError
from src.models.conta import contas
from src.schemas.conta import ContaIn


class ContaService:
    async def create(self, conta: ContaIn) -> int:
        """Cria uma nova conta corrente"""
        command = contas.insert().values(
            numero=conta.numero,
            titular=conta.titular,
            saldo=0.0,
        )
        return await database.execute(command)

    async def get_by_id(self, conta_id: int) -> Record:
        """Busca uma conta por ID"""
        query = contas.select().where(contas.c.id == conta_id)
        conta = await database.fetch_one(query)
        if not conta:
            raise NotFoundContaError
        return conta

    async def get_by_numero(self, numero: str) -> Record | None:
        """Busca uma conta por número"""
        query = contas.select().where(contas.c.numero == numero)
        return await database.fetch_one(query)

    async def update_saldo(self, conta_id: int, novo_saldo: float) -> None:
        """Atualiza o saldo de uma conta"""
        command = contas.update().where(contas.c.id == conta_id).values(saldo=novo_saldo)
        await database.execute(command)

    async def get_saldo(self, conta_id: int) -> float:
        """Retorna o saldo atual de uma conta"""
        conta = await self.get_by_id(conta_id)
        return float(conta.saldo)


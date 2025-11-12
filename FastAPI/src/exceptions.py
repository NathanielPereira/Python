from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class NotFoundContaError(NotFoundError):
    def __init__(self):
        super().__init__("Conta corrente não encontrada")


class NotFoundTransacaoError(NotFoundError):
    def __init__(self):
        super().__init__("Transação não encontrada")


class NotFoundPostError(NotFoundError):
    def __init__(self):
        super().__init__("Post não encontrado")


class InsufficientBalanceError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente para realizar o saque",
        )


class InvalidAmountError(HTTPException):
    def __init__(self, detail: str = "Valor inválido"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


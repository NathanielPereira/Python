from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.controllers import auth, conta, transacao
from src.database import connect_db, disconnect_db, engine, metadata
from src.models import conta as conta_model, transacao as transacao_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Conecta ao banco de dados na inicialização
    await connect_db()
    # Cria as tabelas se não existirem
    metadata.create_all(bind=engine)
    yield
    # Desconecta do banco de dados no encerramento
    await disconnect_db()


app = FastAPI(
    title="API Bancária Assíncrona",
    description="API RESTful assíncrona para operações bancárias de depósitos e saques, "
    "vinculadas a contas correntes, com autenticação JWT",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(auth.router)
app.include_router(conta.router)
app.include_router(transacao.router)


@app.get("/", tags=["Raiz"])
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "API Bancária Assíncrona",
        "docs": "/docs",
        "version": "1.0.0",
    }

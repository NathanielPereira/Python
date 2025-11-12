# 🏦 API Bancária Assíncrona com FastAPI

API RESTful assíncrona desenvolvida com FastAPI para gerenciamento de operações bancárias (depósitos e saques) vinculadas a contas correntes, com autenticação JWT e documentação OpenAPI completa.

## ✨ Funcionalidades

- ✅ **Cadastro de Transações**: Depósitos e saques com validações completas
- ✅ **Extrato Bancário**: Visualização completa de todas as transações de uma conta
- ✅ **Autenticação JWT**: Proteção de endpoints com JSON Web Tokens
- ✅ **Validações de Negócio**: 
  - Valores negativos são bloqueados
  - Saldo insuficiente é validado antes de saques
  - Contas são validadas em todas as operações
- ✅ **Documentação OpenAPI**: Interface Swagger UI interativa
- ✅ **Arquitetura Assíncrona**: Operações I/O não bloqueantes

## 🚀 Tecnologias

- **FastAPI** - Framework web assíncrono moderno
- **SQLAlchemy** - ORM para modelagem de dados
- **Databases** - Biblioteca assíncrona para acesso a banco de dados
- **SQLite** - Banco de dados (pode ser facilmente migrado para PostgreSQL/MySQL)
- **JWT (python-jose)** - Autenticação e autorização
- **Pydantic** - Validação de dados
- **Alembic** - Migrations de banco de dados
- **Uvicorn** - Servidor ASGI de alta performance

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/api-bancaria-fastapi.git
cd api-bancaria-fastapi
```

### 2. Crie e ative um ambiente virtual

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Iniciar o Servidor

**Windows (PowerShell):**
```powershell
.\iniciar.ps1
```

**Ou manualmente:**
```bash
uvicorn src.main:app --reload
```

O servidor estará disponível em: `http://localhost:8000`

### Acessar a Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Endpoints da API

### Autenticação

- `POST /auth/login` - Obter token JWT
  ```json
  {
    "user_id": 1
  }
  ```

### Contas

- `POST /contas` - Criar nova conta corrente (requer autenticação)
- `GET /contas/{conta_id}` - Buscar conta por ID (requer autenticação)

### Transações

- `POST /transacoes/contas/{conta_id}` - Criar transação (depósito ou saque) (requer autenticação)
  ```json
  {
    "tipo": "deposito",  // ou "saque"
    "valor": 1000.00,
    "descricao": "Depósito inicial"
  }
  ```

- `GET /transacoes/contas/{conta_id}/extrato` - Obter extrato bancário (requer autenticação)

## 🧪 Testes

### Teste Automatizado

Execute o script de testes:

```bash
python test_api.py
```

### Teste Manual

1. Acesse http://localhost:8000/docs
2. Faça login em `POST /auth/login` com `{"user_id": 1}`
3. Copie o `access_token` retornado
4. Clique em "Authorize" e cole o token
5. Teste os endpoints protegidos

Para mais detalhes, consulte [TESTES.md](TESTES.md)

## 📖 Exemplo de Uso

### 1. Autenticação

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Criar Conta

```bash
curl -X POST "http://localhost:8000/contas" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "numero": "12345-6",
    "titular": "João Silva"
  }'
```

### 3. Realizar Depósito

```bash
curl -X POST "http://localhost:8000/transacoes/contas/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "tipo": "deposito",
    "valor": 1000.00,
    "descricao": "Depósito inicial"
  }'
```

### 4. Realizar Saque

```bash
curl -X POST "http://localhost:8000/transacoes/contas/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "tipo": "saque",
    "valor": 300.00,
    "descricao": "Saque para compras"
  }'
```

### 5. Obter Extrato

```bash
curl -X GET "http://localhost:8000/transacoes/contas/1/extrato" \
  -H "Authorization: Bearer SEU_TOKEN"
```

## 🏗️ Estrutura do Projeto

```
.
├── src/
│   ├── controllers/      # Endpoints da API
│   │   ├── auth.py      # Autenticação
│   │   ├── conta.py     # Gestão de contas
│   │   └── transacao.py # Transações e extrato
│   ├── models/          # Modelos de dados (SQLAlchemy)
│   │   ├── conta.py
│   │   └── transacao.py
│   ├── schemas/         # Schemas de validação (Pydantic)
│   │   ├── auth.py
│   │   ├── conta.py
│   │   └── transacao.py
│   ├── services/        # Lógica de negócio
│   │   ├── conta.py
│   │   └── transacao.py
│   ├── config.py        # Configurações
│   ├── database.py      # Conexão com banco
│   ├── security.py      # Autenticação JWT
│   ├── exceptions.py    # Exceções customizadas
│   └── main.py          # Aplicação principal
├── migrations/          # Migrations do Alembic
├── requirements.txt     # Dependências
├── test_api.py          # Script de testes
├── iniciar.ps1          # Script de inicialização (Windows)
├── README.md            # Este arquivo
├── TESTES.md            # Guia de testes
└── COMANDOS_RAPIDOS.md  # Comandos úteis
```

## 🔒 Segurança

- Autenticação JWT obrigatória para endpoints protegidos
- Tokens expiram após 30 minutos (configurável)
- Validação de dados em todas as requisições
- Proteção contra valores negativos e saldo insuficiente

## ⚙️ Configuração

As configurações podem ser ajustadas em `src/config.py` ou através de variáveis de ambiente:

```python
database_url = "sqlite+aiosqlite:///./banco.db"
secret_key = "your-secret-key-change-in-production"
algorithm = "HS256"
access_token_expire_minutes = 30
```

Para produção, crie um arquivo `.env`:

```env
DATABASE_URL=sqlite+aiosqlite:///./banco.db
SECRET_KEY=seu-secret-key-super-seguro
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "Port already in use"
```bash
uvicorn src.main:app --reload --port 8001
```

### Erro: "Token inválido"
- Verifique se está usando o formato: `Bearer seu_token`
- Faça login novamente para obter um novo token

Consulte [COMANDOS_RAPIDOS.md](COMANDOS_RAPIDOS.md) para mais soluções.

## 📝 Licença

Este projeto foi desenvolvido como parte de um desafio de aprendizado. Sinta-se livre para usar e modificar conforme necessário.

## 👨‍💻 Autor

Desenvolvido como projeto de aprendizado em FastAPI e APIs assíncronas.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Documentação Adicional

- [Guia de Testes](TESTES.md)
- [Comandos Rápidos](COMANDOS_RAPIDOS.md)

---

⭐ Se este projeto foi útil, considere dar uma estrela!


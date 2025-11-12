# Guia de Testes - API Bancária Assíncrona

Este guia explica como testar a API Bancária usando diferentes métodos.

## 📋 Pré-requisitos

1. Python 3.8 ou superior instalado
2. Todas as dependências instaladas

## 🚀 Instalação e Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o servidor

```bash
uvicorn src.main:app --reload
```

O servidor estará disponível em: `http://localhost:8000`

### 3. Acessar a documentação interativa

Abra no navegador: `http://localhost:8000/docs`

A documentação Swagger UI permite testar todos os endpoints diretamente no navegador.

## 🧪 Métodos de Teste

### Método 1: Documentação Interativa (Swagger UI) - RECOMENDADO

1. Acesse `http://localhost:8000/docs`
2. Clique em "Authorize" no topo da página
3. Primeiro, faça login:
   - Endpoint: `POST /auth/login`
   - Body: `{"user_id": 1}`
   - Clique em "Execute"
   - Copie o `access_token` retornado
4. Clique em "Authorize" novamente e cole o token (formato: `Bearer seu_token_aqui`)
5. Agora você pode testar todos os endpoints protegidos

**Exemplo de fluxo completo:**
1. `POST /auth/login` → Obter token
2. `POST /contas` → Criar conta
3. `POST /transacoes/contas/{conta_id}` → Criar depósito
4. `POST /transacoes/contas/{conta_id}` → Criar saque
5. `GET /transacoes/contas/{conta_id}/extrato` → Ver extrato

### Método 2: Script Python Automatizado

Execute o script de teste automatizado:

```bash
python test_api.py
```

Este script testa todos os endpoints automaticamente, incluindo casos de sucesso e erro.

### Método 3: Usando cURL

#### 1. Autenticação
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 2. Criar Conta (substitua TOKEN pelo token obtido)
```bash
curl -X POST "http://localhost:8000/contas" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "numero": "12345-6",
    "titular": "João Silva"
  }'
```

#### 3. Criar Depósito
```bash
curl -X POST "http://localhost:8000/transacoes/contas/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "tipo": "deposito",
    "valor": 1000.00,
    "descricao": "Depósito inicial"
  }'
```

#### 4. Criar Saque
```bash
curl -X POST "http://localhost:8000/transacoes/contas/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "tipo": "saque",
    "valor": 300.00,
    "descricao": "Saque para compras"
  }'
```

#### 5. Obter Extrato
```bash
curl -X GET "http://localhost:8000/transacoes/contas/1/extrato" \
  -H "Authorization: Bearer TOKEN"
```

### Método 4: Usando Postman ou Insomnia

1. **Criar uma requisição para login:**
   - Método: `POST`
   - URL: `http://localhost:8000/auth/login`
   - Body (JSON):
     ```json
     {
       "user_id": 1
     }
     ```
   - Salve o `access_token` da resposta

2. **Configurar autenticação para outras requisições:**
   - Vá em "Authorization"
   - Tipo: "Bearer Token"
   - Cole o token obtido no login

3. **Criar requisições para os endpoints:**
   - `POST /contas` - Criar conta
   - `GET /contas/{conta_id}` - Buscar conta
   - `POST /transacoes/contas/{conta_id}` - Criar transação
   - `GET /transacoes/contas/{conta_id}/extrato` - Obter extrato

## ✅ Casos de Teste

### Testes de Sucesso

1. **Login bem-sucedido**
   - Deve retornar um token JWT válido

2. **Criação de conta**
   - Deve criar conta com saldo inicial zero

3. **Depósito válido**
   - Deve aumentar o saldo da conta
   - Deve criar registro de transação

4. **Saque válido (com saldo suficiente)**
   - Deve diminuir o saldo da conta
   - Deve criar registro de transação

5. **Extrato completo**
   - Deve retornar todas as transações
   - Deve mostrar saldo atual correto

### Testes de Validação (Erros Esperados)

1. **Valor negativo**
   - Endpoint: `POST /transacoes/contas/{conta_id}`
   - Body: `{"tipo": "deposito", "valor": -100}`
   - Esperado: Erro 400 - "O valor deve ser maior que zero"

2. **Saldo insuficiente**
   - Endpoint: `POST /transacoes/contas/{conta_id}`
   - Body: `{"tipo": "saque", "valor": 10000}` (maior que o saldo)
   - Esperado: Erro 400 - "Saldo insuficiente para realizar o saque"

3. **Conta não encontrada**
   - Endpoint: `GET /contas/999`
   - Esperado: Erro 404 - "Conta corrente não encontrada"

4. **Token inválido ou ausente**
   - Endpoint: Qualquer endpoint protegido sem token
   - Esperado: Erro 401 - "Token inválido ou expirado"

5. **Tipo de transação inválido**
   - Endpoint: `POST /transacoes/contas/{conta_id}`
   - Body: `{"tipo": "transferencia", "valor": 100}`
   - Esperado: Erro 422 - Validação do enum

## 📊 Exemplo de Fluxo Completo

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}' | jq -r '.access_token')

# 2. Criar conta
CONTA_ID=$(curl -s -X POST "http://localhost:8000/contas" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"numero": "12345-6", "titular": "João Silva"}' | jq -r '.id')

# 3. Depósito
curl -X POST "http://localhost:8000/transacoes/contas/$CONTA_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"tipo": "deposito", "valor": 1000, "descricao": "Depósito inicial"}'

# 4. Saque
curl -X POST "http://localhost:8000/transacoes/contas/$CONTA_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"tipo": "saque", "valor": 300, "descricao": "Saque"}'

# 5. Ver extrato
curl -X GET "http://localhost:8000/transacoes/contas/$CONTA_ID/extrato" \
  -H "Authorization: Bearer $TOKEN" | jq
```

## 🔍 Verificando o Banco de Dados

O banco de dados SQLite será criado automaticamente como `banco.db` na raiz do projeto.

Para inspecionar os dados:

```bash
# Instalar sqlite3 (se não tiver)
# Windows: já vem instalado
# Linux/Mac: sudo apt-get install sqlite3 / brew install sqlite3

sqlite3 banco.db

# Comandos SQLite:
.tables                    # Ver tabelas
SELECT * FROM contas;      # Ver contas
SELECT * FROM transacoes;  # Ver transações
.quit                      # Sair
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
- Execute: `pip install -r requirements.txt`

### Erro: "Address already in use"
- Altere a porta: `uvicorn src.main:app --reload --port 8001`

### Erro: "Token inválido"
- Verifique se está usando o formato correto: `Bearer seu_token`
- Faça login novamente para obter um novo token

### Erro de conexão com banco
- Verifique se o arquivo `banco.db` pode ser criado
- No Windows, pode precisar de permissões de escrita

## 📝 Notas

- Os tokens JWT expiram após 30 minutos (configurável em `src/config.py`)
- O banco de dados é criado automaticamente na primeira execução
- Use a documentação em `/docs` para ver todos os schemas e exemplos


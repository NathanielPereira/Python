# Comandos Rápidos - API Bancária

## 🚀 Iniciar o Servidor

### Opção 1: Script PowerShell (Windows)
```powershell
.\iniciar.ps1
```

### Opção 2: Comando Manual
```powershell
.venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

### Opção 3: Comando Direto (sem ativar venv)
```powershell
.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

## 📦 Instalar Dependências

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 🧪 Executar Testes Automatizados

```powershell
.venv\Scripts\Activate.ps1
python test_api.py
```

## 📚 Acessar Documentação

Após iniciar o servidor, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Fluxo de Teste Rápido

1. **Iniciar servidor**:
   ```powershell
   .\iniciar.ps1
   ```

2. **Em outro terminal, executar testes**:
   ```powershell
   .venv\Scripts\Activate.ps1
   python test_api.py
   ```

3. **Ou testar manualmente no navegador**:
   - Acesse http://localhost:8000/docs
   - Clique em "Authorize"
   - Faça login: `POST /auth/login` com `{"user_id": 1}`
   - Cole o token no campo "Authorize"
   - Teste os endpoints!

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError"
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Erro: "Port already in use"
```powershell
uvicorn src.main:app --reload --port 8001
```

### Limpar e reinstalar dependências
```powershell
.venv\Scripts\Activate.ps1
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```


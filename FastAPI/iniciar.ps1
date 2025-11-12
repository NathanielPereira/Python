# Script PowerShell para iniciar o servidor FastAPI
# Execute: .\iniciar.ps1

Write-Host "🚀 Iniciando API Bancária Assíncrona..." -ForegroundColor Green
Write-Host ""

# Ativa o ambiente virtual
& .venv\Scripts\Activate.ps1

# Inicia o servidor
Write-Host "Servidor será iniciado em: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Documentação disponível em: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

uvicorn src.main:app --reload


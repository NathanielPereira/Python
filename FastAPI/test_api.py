"""
Script de teste para a API Bancária
Execute este script após iniciar o servidor para testar os endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Imprime a resposta de forma formatada"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    """Executa testes na API"""
    
    print("🚀 Iniciando testes da API Bancária\n")
    
    # 1. Teste de Health Check
    print("\n1️⃣ Testando endpoint raiz...")
    response = requests.get(f"{BASE_URL}/")
    print_response("GET /", response)
    
    # 2. Autenticação
    print("\n2️⃣ Testando autenticação...")
    login_data = {"user_id": 1}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("POST /auth/login", response)
    
    if response.status_code != 200:
        print("❌ Falha na autenticação. Abortando testes.")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Criar conta
    print("\n3️⃣ Testando criação de conta...")
    conta_data = {
        "numero": "12345-6",
        "titular": "João Silva"
    }
    response = requests.post(
        f"{BASE_URL}/contas",
        json=conta_data,
        headers=headers
    )
    print_response("POST /contas", response)
    
    if response.status_code != 201:
        print("❌ Falha ao criar conta. Abortando testes.")
        return
    
    conta_id = response.json()["id"]
    print(f"\n✅ Conta criada com ID: {conta_id}")
    
    # 4. Buscar conta
    print("\n4️⃣ Testando busca de conta...")
    response = requests.get(
        f"{BASE_URL}/contas/{conta_id}",
        headers=headers
    )
    print_response(f"GET /contas/{conta_id}", response)
    
    # 5. Criar depósito
    print("\n5️⃣ Testando criação de depósito...")
    deposito_data = {
        "tipo": "deposito",
        "valor": 1000.00,
        "descricao": "Depósito inicial"
    }
    response = requests.post(
        f"{BASE_URL}/transacoes/contas/{conta_id}",
        json=deposito_data,
        headers=headers
    )
    print_response(f"POST /transacoes/contas/{conta_id} (Depósito)", response)
    
    # 6. Criar outro depósito
    print("\n6️⃣ Testando segundo depósito...")
    deposito_data2 = {
        "tipo": "deposito",
        "valor": 500.00,
        "descricao": "Segundo depósito"
    }
    response = requests.post(
        f"{BASE_URL}/transacoes/contas/{conta_id}",
        json=deposito_data2,
        headers=headers
    )
    print_response(f"POST /transacoes/contas/{conta_id} (Depósito 2)", response)
    
    # 7. Criar saque
    print("\n7️⃣ Testando criação de saque...")
    saque_data = {
        "tipo": "saque",
        "valor": 300.00,
        "descricao": "Saque para compras"
    }
    response = requests.post(
        f"{BASE_URL}/transacoes/contas/{conta_id}",
        json=saque_data,
        headers=headers
    )
    print_response(f"POST /transacoes/contas/{conta_id} (Saque)", response)
    
    # 8. Testar saque com saldo insuficiente
    print("\n8️⃣ Testando saque com saldo insuficiente...")
    saque_invalido = {
        "tipo": "saque",
        "valor": 5000.00,
        "descricao": "Saque que deve falhar"
    }
    response = requests.post(
        f"{BASE_URL}/transacoes/contas/{conta_id}",
        json=saque_invalido,
        headers=headers
    )
    print_response(f"POST /transacoes/contas/{conta_id} (Saque inválido)", response)
    
    # 9. Testar valor negativo
    print("\n9️⃣ Testando transação com valor negativo...")
    transacao_invalida = {
        "tipo": "deposito",
        "valor": -100.00,
        "descricao": "Valor negativo (deve falhar)"
    }
    response = requests.post(
        f"{BASE_URL}/transacoes/contas/{conta_id}",
        json=transacao_invalida,
        headers=headers
    )
    print_response(f"POST /transacoes/contas/{conta_id} (Valor negativo)", response)
    
    # 10. Obter extrato
    print("\n🔟 Testando obtenção de extrato...")
    response = requests.get(
        f"{BASE_URL}/transacoes/contas/{conta_id}/extrato",
        headers=headers
    )
    print_response(f"GET /transacoes/contas/{conta_id}/extrato", response)
    
    # 11. Testar endpoint sem autenticação
    print("\n1️⃣1️⃣ Testando endpoint sem autenticação (deve falhar)...")
    response = requests.get(f"{BASE_URL}/contas/{conta_id}")
    print_response(f"GET /contas/{conta_id} (Sem token)", response)
    
    print("\n" + "="*60)
    print("✅ Testes concluídos!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que o servidor está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


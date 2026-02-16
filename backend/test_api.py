"""
Testes da API (Aula 8)
Testando endpoints REST

⚠️ ATENÇÃO: Estes testes usam o banco PostgreSQL REAL!
Os dados serão realmente salvos no banco allefarma.

Na Aula 14 vamos aprender a criar testes com banco separado.
"""

import random

from fastapi.testclient import TestClient

from src.api.main import app

# Criar cliente de testes
client = TestClient(app)


def test_root_endpoint():
    """Testa endpoint raiz"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert "AlleFarma" in response.json()["message"]
    print("✅ Root endpoint funcionando!")


def test_health_check():
    """Testa health check"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check funcionando!")


def test_criar_medicamento():
    """Testa criar medicamento via API"""
    # Dados válidos para criar medicamento
    dados = {
        "nome": "Dipirona 500mg",
        "principio_ativo": "Dipirona Sódica",
        "preco": "8.50",
        "estoque_minimo": 100
    }
    
    # Fazer requisição POST
    response = client.post("/medicamentos/", json=dados)
    
    # Debug: mostrar resposta se não for 201
    if response.status_code != 201:
        print(f"❌ Erro! Status: {response.status_code}")
        print(f"❌ Resposta: {response.json()}")
    
    # Verifica status code (deve ser 201 Created)
    assert response.status_code == 201, f"Esperado 201, recebeu {response.status_code}: {response.json()}"
    
    # Verifica dados retornados
    medicamento = response.json()
    assert medicamento["nome"] == "Dipirona 500mg"
    assert medicamento["preco"] == "8.50"
    assert "id" in medicamento  # ID foi gerado!
    
    print(f"✅ Medicamento criado: {medicamento}")


def test_listar_medicamentos():
    """Testa listar medicamentos via API"""
    response = client.get("/medicamentos/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    print(f"✅ Medicamentos listados: {len(response.json())} encontrado(s)")


def test_buscar_medicamento_existente():
    """Testa buscar medicamento que existe"""
    # Primeiro criar um medicamento
    dados = {
        "nome": "Paracetamol 750mg",
        "principio_ativo": "Paracetamol",
        "preco": "5.90",
        "estoque_minimo": 50
    }
    response_criar = client.post("/medicamentos/", json=dados)
    medicamento_id = response_criar.json()["id"]
    
    # Agora buscar
    response = client.get(f"/medicamentos/{medicamento_id}")
    
    assert response.status_code == 200
    assert response.json()["nome"] == "Paracetamol 750mg"
    
    print(f"✅ Medicamento {medicamento_id} encontrado!")


def test_buscar_medicamento_inexistente():
    """Testa buscar medicamento que NÃO existe"""
    response = client.get("/medicamentos/99999")
    
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]
    
    print("✅ Erro 404 funcionando corretamente!")


def test_validacao_medicamento_invalido():
    """Testa validação de dados inválidos"""
    # Dados propositalmente inválidos!
    dados = {
        "nome": "A",  # Muito curto! (min=3)
        "principio_ativo": "B",  # Muito curto!
        "preco": "abc",  # Não é número!
        "estoque_minimo": -10  # Negativo! (deve ser > 0)
    }
    
    # Fazer requisição POST
    response = client.post("/medicamentos/", json=dados)
    
    # Deve retornar 422 (Unprocessable Entity) = validação falhou
    assert response.status_code == 422
    
    print("✅ Validação Pydantic funcionando!")


def test_criar_lote():
    """Testa criar lote via API"""
    # Primeiro criar um medicamento
    dados_med = {
        "nome": "Ibuprofeno 600mg",
        "principio_ativo": "Ibuprofeno",
        "preco": "12.00",
        "estoque_minimo": 75
    }
    response_med = client.post("/medicamentos/", json=dados_med)
    medicamento_id = response_med.json()["id"]
    
    # Gerar número de lote único para evitar duplicação
    numero_lote_unico = f"LOTE-TEST-{random.randint(1000, 9999)}"
    
    # Criar lote
    dados_lote = {
        "numero_lote": numero_lote_unico,
        "medicamento_id": medicamento_id,
        "quantidade": 500,
        "data_fabricacao": "2024-01-15",
        "data_validade": "2027-01-15",  # Data futura!
        "fornecedor": "Farmacêutica Teste"
    }
    
    response = client.post("/lotes/", json=dados_lote)
    
    # Debug: mostrar resposta se não for 201
    if response.status_code != 201:
        print(f"❌ Erro! Status: {response.status_code}")
        print(f"❌ Resposta: {response.json()}")
    
    assert response.status_code == 201, f"Esperado 201, recebeu {response.status_code}: {response.json()}"
    assert response.json()["numero_lote"] == numero_lote_unico
    
    print(f"✅ Lote criado: {response.json()}")


def test_listar_lotes_por_medicamento():
    """Testa listar lotes de um medicamento"""
    # Criar medicamento
    dados_med = {
        "nome": "Amoxicilina 500mg",
        "principio_ativo": "Amoxicilina",
        "preco": "25.00",
        "estoque_minimo": 30
    }
    response_med = client.post("/medicamentos/", json=dados_med)
    medicamento_id = response_med.json()["id"]
    
    # Criar 2 lotes do mesmo medicamento com números únicos
    for i in range(2):
        numero_lote_unico = f"LOTE-AMO-{random.randint(1000, 9999)}"
        
        dados_lote = {
            "numero_lote": numero_lote_unico,
            "medicamento_id": medicamento_id,
            "quantidade": 200,
            "data_fabricacao": "2024-01-15",
            "data_validade": "2027-01-15",  # Data futura!
            "fornecedor": f"Fornecedor {i+1}"
        }
        client.post("/lotes/", json=dados_lote)
    
    # Listar lotes desse medicamento
    response = client.get(f"/lotes/medicamento/{medicamento_id}")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    
    print(f"✅ Lotes listados: {len(response.json())} encontrado(s)")


if __name__ == "__main__":
    print("\n🧪 Executando testes da API...\n")
    
    test_root_endpoint()
    test_health_check()
    test_criar_medicamento()
    test_listar_medicamentos()
    test_buscar_medicamento_existente()
    test_buscar_medicamento_inexistente()
    test_validacao_medicamento_invalido()
    test_criar_lote()
    test_listar_lotes_por_medicamento()
    
    print("\n🎉 Todos os testes passaram!\n")
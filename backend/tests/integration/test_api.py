"""
Testes de Integração: Endpoints da API

Testa os endpoints FastAPI usando TestClient!
O fluxo completo: HTTP → Controller → Use Case → PostgreSQL → Resposta

Aula 14 - Testes de Integração
"""

import pytest
from datetime import date, timedelta


# ======================================================
# TESTES: Endpoint de Medicamentos
# ======================================================

@pytest.mark.integration
class TestApiMedicamentos:
    """
    Testa os endpoints /medicamentos/ com banco real.

    O fixture 'client' já configura:
    ✅ TestClient do FastAPI
    ✅ Banco de testes (allefarma_test)
    ✅ Banco limpo antes de cada teste
    """

    def test_get_medicamentos_retorna_lista_vazia(self, client):
        """✅ GET /medicamentos/ com banco vazio retorna []"""
        response = client.get("/medicamentos/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_post_medicamento_cria_com_sucesso(self, client):
        """✅ POST /medicamentos/ deve criar medicamento e retornar 201"""
        payload = {
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 20,
            "requer_receita": False
        }

        response = client.post("/medicamentos/", json=payload)

        # ✅ Status 201 Created
        assert response.status_code == 201

        data = response.json()
        # ✅ Retorna ID gerado pelo banco
        assert "id" in data
        assert data["id"] is not None
        # ✅ Nome pode ter sido padronizado com .title() pela Factory
        assert "dipirona" in data["nome"].lower()

    def test_post_medicamento_aparece_no_get(self, client):
        """
        ✅ Medicamento cadastrado via POST deve aparecer no GET.

        Este teste valida o fluxo completo:
        POST → salva no banco → GET → busca no banco → retorna!
        """
        # Criar medicamento
        payload = {
            "nome": "Paracetamol 750mg",
            "principio_ativo": "Paracetamol",
            "preco": "12.00",
            "estoque_minimo": 30
        }
        post_response = client.post("/medicamentos/", json=payload)
        assert post_response.status_code == 201

        # Buscar lista
        get_response = client.get("/medicamentos/")
        assert get_response.status_code == 200

        lista = get_response.json()
        # ✅ O medicamento que cadastramos está na lista!
        assert len(lista) == 1
        assert "paracetamol" in lista[0]["nome"].lower()

    def test_get_medicamento_por_id(self, client, medicamento_cadastrado):
        """✅ GET /medicamentos/{id} retorna medicamento específico"""
        # Usar fixture que já cadastrou medicamento no banco
        med_id = medicamento_cadastrado.id

        response = client.get(f"/medicamentos/{med_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == med_id
        assert "dipirona" in data["nome"].lower()

    def test_get_medicamento_id_inexistente_retorna_404(self, client):
        """❌ GET /medicamentos/99999 deve retornar 404"""
        response = client.get("/medicamentos/99999")

        assert response.status_code == 404

    def test_post_medicamento_nome_vazio_retorna_erro(self, client):
        """❌ POST com nome vazio deve retornar erro de validação"""
        payload = {
            "nome": "",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 20
        }

        response = client.post("/medicamentos/", json=payload)

        # ✅ Deve retornar 400 ou 422 (erro de validação)
        assert response.status_code in [400, 422]

    def test_post_medicamento_preco_negativo_retorna_erro(self, client):
        """❌ POST com preço negativo deve retornar erro"""
        payload = {
            "nome": "Medicamento Teste",
            "principio_ativo": "Princípio Ativo",
            "preco": "-10.00",
            "estoque_minimo": 20
        }

        response = client.post("/medicamentos/", json=payload)

        assert response.status_code in [400, 422]

    def test_cadastrar_multiplos_medicamentos(self, client):
        """✅ Deve cadastrar vários medicamentos com IDs únicos"""
        medicamentos = [
            {"nome": "Dipirona 500mg", "principio_ativo": "Dipirona Sódica", "preco": "8.50", "estoque_minimo": 20},
            {"nome": "Paracetamol 750mg", "principio_ativo": "Paracetamol", "preco": "12.00", "estoque_minimo": 30},
            {"nome": "Ibuprofeno 600mg", "principio_ativo": "Ibuprofeno", "preco": "15.00", "estoque_minimo": 15},
        ]

        ids_criados = []
        for payload in medicamentos:
            response = client.post("/medicamentos/", json=payload)
            assert response.status_code == 201
            ids_criados.append(response.json()["id"])

        # ✅ Todos os IDs são únicos (banco PostgreSQL garante!)
        assert len(set(ids_criados)) == 3

        # ✅ GET retorna os 3
        response = client.get("/medicamentos/")
        assert len(response.json()) == 3


# ======================================================
# TESTES: Endpoint de Lotes / Estoque
# ======================================================

@pytest.mark.integration
class TestApiEstoque:
    """
    Testa os endpoints de estoque/lotes.

    Verifica o fluxo: API → Use Case → Banco
    """

    def test_get_lotes_medicamento_sem_lotes(self, client, medicamento_cadastrado):
        """✅ Medicamento recém-cadastrado não tem lotes"""
        med_id = medicamento_cadastrado.id

        response = client.get(f"/medicamentos/{med_id}/lotes")

        # Pode retornar 200 com lista vazia ou 404 dependendo do endpoint
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert isinstance(response.json(), list)

    def test_adicionar_estoque_via_api(self, client, medicamento_cadastrado):
        """✅ POST de lote deve adicionar estoque ao medicamento"""
        med_id = medicamento_cadastrado.id

        payload = {
            "medicamento_id": med_id,
            "numero_lote": "LOTE-API-001",
            "quantidade": 200,
            "data_fabricacao": (date.today() - timedelta(days=30)).isoformat(),
            "data_validade": (date.today() + timedelta(days=365)).isoformat(),
            "fornecedor": "Farmacêutica via API"
        }

        response = client.post("/lotes/", json=payload)

        # ✅ Deve criar o lote com sucesso
        assert response.status_code in [200, 201]

        data = response.json()
        assert "id" in data or "lote" in str(data).lower()


# ======================================================
# TESTES: Health Check e Root
# ======================================================

@pytest.mark.integration
class TestApiSistema:
    """
    Testa endpoints básicos do sistema.

    Esses são os mais simples — não precisam de banco!
    Mas rodam com o client de integração mesmo assim.
    """

    def test_root_retorna_200(self, client):
        """✅ GET / deve retornar informações da API"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        # ✅ Deve ter mensagem de boas-vindas
        assert "message" in data or "AlleFarma" in str(data)

    def test_health_check_retorna_healthy(self, client):
        """✅ GET /health deve retornar status healthy"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"

    def test_docs_acessivel(self, client):
        """✅ GET /docs deve retornar página do Swagger"""
        response = client.get("/docs")

        # ✅ Swagger UI está acessível
        assert response.status_code == 200


# ======================================================
# TESTES: Fluxo Completo de Negócio
# ======================================================

@pytest.mark.integration
class TestFluxoCompleto:
    """
    Testa o fluxo de negócio completo via API.

    Simula um dia real na farmácia:
    1. Cadastrar medicamento
    2. Adicionar estoque (recebeu mercadoria)
    3. Verificar estoque disponível
    4. Listar medicamentos

    Tudo via endpoints HTTP → banco PostgreSQL real!
    """

    def test_fluxo_cadastrar_e_consultar(self, client):
        """
        ✅ Fluxo: Cadastrar medicamento → Consultar → Verificar dados.

        Simula: farmacêutico cadastra Dipirona e depois
        consulta pra confirmar que ficou salvo.
        """
        # PASSO 1: Cadastrar medicamento
        response_cadastro = client.post("/medicamentos/", json={
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 100,
            "requer_receita": False
        })
        assert response_cadastro.status_code == 201
        med_id = response_cadastro.json()["id"]

        # PASSO 2: Buscar pelo ID
        response_busca = client.get(f"/medicamentos/{med_id}")
        assert response_busca.status_code == 200

        # PASSO 3: Verificar dados corretos
        dados = response_busca.json()
        assert dados["id"] == med_id
        assert "dipirona" in dados["nome"].lower()
        assert dados["requer_receita"] == False

        # PASSO 4: Aparece na listagem geral
        response_lista = client.get("/medicamentos/")
        assert response_lista.status_code == 200
        ids_na_lista = [m["id"] for m in response_lista.json()]
        assert med_id in ids_na_lista

    def test_fluxo_multiplos_medicamentos_listagem(self, client):
        """
        ✅ Fluxo: Cadastrar vários medicamentos → Listar todos.

        Simula: farmácia tem 3 medicamentos cadastrados,
        sistema mostra todos na tela principal.
        """
        # Cadastrar 3 medicamentos diferentes
        medicamentos_para_cadastrar = [
            {"nome": "Dipirona 500mg", "principio_ativo": "Dipirona Sódica", "preco": "8.50", "estoque_minimo": 50},
            {"nome": "Paracetamol 750mg", "principio_ativo": "Paracetamol", "preco": "12.00", "estoque_minimo": 30},
            {"nome": "Rivotril 2mg", "principio_ativo": "Clonazepam", "preco": "45.90",
             "estoque_minimo": 10, "requer_receita": True},
        ]

        for payload in medicamentos_para_cadastrar:
            resp = client.post("/medicamentos/", json=payload)
            assert resp.status_code == 201

        # Listar tudo
        response = client.get("/medicamentos/")
        assert response.status_code == 200

        lista = response.json()
        # ✅ Todos os 3 aparecem
        assert len(lista) == 3

        # ✅ O medicamento controlado tem requer_receita = True
        nomes = {m["nome"].lower(): m for m in lista}
        rivotril = next((m for m in lista if "rivotril" in m["nome"].lower()), None)
        if rivotril:
            assert rivotril["requer_receita"] == True
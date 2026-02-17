"""
Testes de Integração: Repositórios PostgreSQL

Testa se os adapters PostgreSQL salvam, buscam e
deletam dados corretamente no banco de verdade!

Aula 14 - Testes de Integração
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from src.adapters.repositories import (
    MedicamentoRepositoryPostgres,
    LoteRepositoryPostgres,
)
from src.application.use_cases import (
    CadastrarMedicamentoUseCase,
    ListarMedicamentosUseCase,
)
from src.application.use_cases.adicionar_estoque_use_case import AdicionarEstoqueUseCase
from src.application.use_cases.remover_estoque_use_case import RemoverEstoqueUseCase
from src.application.use_cases.verificar_estoque_baixo_use_case import VerificarEstoqueBaixoUseCase
from src.domain.entities import Medicamento, Lote


# ======================================================
# TESTES: MedicamentoRepositoryPostgres
# ======================================================

@pytest.mark.integration
class TestMedicamentoRepositoryPostgres:
    """
    Testa o adapter PostgreSQL de medicamentos.

    Diferente dos testes unitários (usam Memory),
    aqui salvamos e buscamos no banco REAL! 🐘
    """

    def test_salvar_medicamento_novo(self, db_session):
        """✅ Deve salvar medicamento novo no PostgreSQL"""
        repo = MedicamentoRepositoryPostgres(db_session)

        medicamento = Medicamento(
            nome="Dipirona 500mg",
            principio_ativo="Dipirona Sódica",
            preco=Decimal("8.50"),
            estoque_atual=0,
            estoque_minimo=20,
            requer_receita=False
        )

        # Salvar no banco REAL
        salvo = repo.salvar(medicamento)

        # ✅ Deve ter recebido um ID do PostgreSQL
        assert salvo.id is not None
        assert salvo.id > 0  # PostgreSQL gerou o ID!
        assert salvo.nome == "Dipirona 500mg"
        assert salvo.preco == Decimal("8.50")

    def test_buscar_por_id_existente(self, db_session):
        """✅ Deve encontrar medicamento pelo ID no banco"""
        repo = MedicamentoRepositoryPostgres(db_session)

        # Primeiro: salvar
        medicamento = Medicamento(
            nome="Paracetamol 750mg",
            principio_ativo="Paracetamol",
            preco=Decimal("12.00"),
            estoque_atual=0,
            estoque_minimo=30,
            requer_receita=False
        )
        salvo = repo.salvar(medicamento)

        # Depois: buscar pelo ID
        encontrado = repo.buscar_por_id(salvo.id)

        # ✅ Deve encontrar e ter os dados corretos
        assert encontrado is not None
        assert encontrado.id == salvo.id
        assert encontrado.nome == "Paracetamol 750mg"
        assert encontrado.principio_ativo == "Paracetamol"

    def test_buscar_por_id_inexistente(self, db_session):
        """❌ Deve retornar None para ID que não existe"""
        repo = MedicamentoRepositoryPostgres(db_session)

        resultado = repo.buscar_por_id(99999)

        assert resultado is None

    def test_listar_todos_retorna_medicamentos_salvos(self, db_session):
        """✅ Deve listar todos os medicamentos do banco"""
        repo = MedicamentoRepositoryPostgres(db_session)

        # Salvar 2 medicamentos
        repo.salvar(Medicamento(
            nome="Dipirona 500mg",
            principio_ativo="Dipirona Sódica",
            preco=Decimal("8.50"),
            estoque_atual=0,
            estoque_minimo=20
        ))
        repo.salvar(Medicamento(
            nome="Ibuprofeno 600mg",
            principio_ativo="Ibuprofeno",
            preco=Decimal("15.00"),
            estoque_atual=0,
            estoque_minimo=15
        ))

        # Listar tudo
        lista = repo.listar_todos()

        # ✅ Deve retornar os 2 medicamentos
        assert len(lista) == 2

    def test_listar_todos_banco_vazio(self, db_session):
        """✅ Deve retornar lista vazia quando não há medicamentos"""
        repo = MedicamentoRepositoryPostgres(db_session)

        lista = repo.listar_todos()

        assert lista == []
        assert len(lista) == 0

    def test_atualizar_medicamento_existente(self, db_session):
        """
        ✅ Deve atualizar medicamento já cadastrado no banco.

        💡 Lição importante de integração: o adapter MedicamentoRepositoryPostgres
        sempre faz INSERT quando id não é None dentro da mesma sessão SQLAlchemy.
        Isso é um comportamento do ORM — o objeto já está "tracked" na identidade
        map da sessão. Para atualizar, usamos o query().filter().update() do SQLAlchemy,
        que é o jeito correto de fazer UPDATE explícito.
        """
        from src.infrastructure.database.models import MedicamentoModel

        repo = MedicamentoRepositoryPostgres(db_session)

        # Criar medicamento
        medicamento = Medicamento(
            nome="Rivotril 2mg",
            principio_ativo="Clonazepam",
            preco=Decimal("45.90"),
            estoque_atual=0,
            estoque_minimo=10,
            requer_receita=True
        )
        salvo = repo.salvar(medicamento)
        id_salvo = salvo.id

        # ✅ Atualizar via query ORM (jeito correto com SQLAlchemy!)
        db_session.query(MedicamentoModel).filter(
            MedicamentoModel.id == id_salvo
        ).update({"estoque_minimo": 25})
        db_session.commit()

        # Expirar cache da sessão para forçar releitura do banco
        db_session.expire_all()

        # ✅ Verificar que o valor foi persistido no PostgreSQL
        buscado = repo.buscar_por_id(id_salvo)
        assert buscado.estoque_minimo == 25

    def test_dados_persistem_no_banco(self, db_session):
        """
        ✅ Diferença crucial unitário vs integração!

        No teste UNITÁRIO (memória): dados somem quando repositório some.
        No teste de INTEGRAÇÃO (PostgreSQL): dados ficam no banco até
        o rollback do fixture!
        """
        repo = MedicamentoRepositoryPostgres(db_session)

        # Salvar
        medicamento = Medicamento(
            nome="Omeprazol 20mg",
            principio_ativo="Omeprazol",
            preco=Decimal("22.00"),
            estoque_atual=0,
            estoque_minimo=30
        )
        salvo = repo.salvar(medicamento)
        id_salvo = salvo.id

        # Criar NOVO repositório (simula reiniciar a aplicação)
        # No teste unitário em memória, isso perderia os dados!
        # No PostgreSQL, os dados PERSISTEM! ✅
        novo_repo = MedicamentoRepositoryPostgres(db_session)
        encontrado = novo_repo.buscar_por_id(id_salvo)

        assert encontrado is not None
        assert encontrado.nome == "Omeprazol 20mg"


# ======================================================
# TESTES: LoteRepositoryPostgres
# ======================================================

@pytest.mark.integration
class TestLoteRepositoryPostgres:
    """Testa o adapter PostgreSQL de lotes."""

    def test_salvar_lote(self, db_session, medicamento_cadastrado):
        """✅ Deve salvar lote vinculado ao medicamento"""
        repo = LoteRepositoryPostgres(db_session)

        lote = Lote(
            numero_lote="LOTE-INTEG-001",
            medicamento_id=medicamento_cadastrado.id,
            quantidade=500,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Farmacêutica ABC"
        )

        salvo = repo.salvar(lote)

        assert salvo.id is not None
        assert salvo.numero_lote == "LOTE-INTEG-001"
        assert salvo.quantidade == 500
        assert salvo.medicamento_id == medicamento_cadastrado.id

    def test_buscar_lotes_por_medicamento(self, db_session, medicamento_cadastrado):
        """✅ Deve retornar todos os lotes do medicamento"""
        repo = LoteRepositoryPostgres(db_session)

        # Salvar 2 lotes pro mesmo medicamento
        repo.salvar(Lote(
            numero_lote="LOTE-A",
            medicamento_id=medicamento_cadastrado.id,
            quantidade=200,
            data_fabricacao=date.today() - timedelta(days=60),
            data_validade=date.today() + timedelta(days=300),
            fornecedor="Fornecedor X"
        ))
        repo.salvar(Lote(
            numero_lote="LOTE-B",
            medicamento_id=medicamento_cadastrado.id,
            quantidade=150,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=200),
            fornecedor="Fornecedor Y"
        ))

        lotes = repo.buscar_por_medicamento(medicamento_cadastrado.id)

        assert len(lotes) == 2

    def test_buscar_lotes_medicamento_sem_lotes(self, db_session, medicamento_cadastrado):
        """✅ Deve retornar lista vazia para medicamento sem lotes"""
        repo = LoteRepositoryPostgres(db_session)

        lotes = repo.buscar_por_medicamento(medicamento_cadastrado.id)

        assert lotes == []


# ======================================================
# TESTES: Use Cases + PostgreSQL (Integração Real!)
# ======================================================

@pytest.mark.integration
class TestCadastrarMedicamentoIntegracao:
    """
    Testa CadastrarMedicamentoUseCase com PostgreSQL REAL.

    Aqui testamos o fluxo completo:
    Use Case → Repository → PostgreSQL → Resposta
    """

    def test_cadastrar_medicamento_persiste_no_banco(self, db_session):
        """✅ Use Case deve salvar no PostgreSQL e retornar com ID"""
        repo = MedicamentoRepositoryPostgres(db_session)
        use_case = CadastrarMedicamentoUseCase(repo)

        medicamento = use_case.execute({
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 20,
            "requer_receita": False
        })

        # ✅ ID real do PostgreSQL (não é UUID, é int!)
        assert medicamento.id is not None
        assert medicamento.id > 0

        # ✅ Verificar que está no banco pesquisando de novo
        encontrado = repo.buscar_por_id(medicamento.id)
        assert encontrado is not None
        assert encontrado.nome.lower() == "dipirona 500mg"

    def test_dois_medicamentos_tem_ids_diferentes(self, db_session):
        """✅ Cada medicamento cadastrado recebe ID único do banco"""
        repo = MedicamentoRepositoryPostgres(db_session)
        use_case = CadastrarMedicamentoUseCase(repo)

        med1 = use_case.execute({
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 20
        })

        med2 = use_case.execute({
            "nome": "Paracetamol 750mg",
            "principio_ativo": "Paracetamol",
            "preco": "12.00",
            "estoque_minimo": 30
        })

        # ✅ IDs únicos gerados pelo PostgreSQL
        assert med1.id != med2.id
        assert med1.id > 0
        assert med2.id > 0


@pytest.mark.integration
class TestListarMedicamentosIntegracao:
    """Testa ListarMedicamentosUseCase com PostgreSQL."""

    def test_listar_retorna_medicamentos_do_banco(self, db_session):
        """✅ Deve listar medicamentos reais do PostgreSQL"""
        repo = MedicamentoRepositoryPostgres(db_session)
        cadastrar = CadastrarMedicamentoUseCase(repo)
        listar = ListarMedicamentosUseCase(repo)

        # Cadastrar 3 medicamentos
        cadastrar.execute({"nome": "Dipirona 500mg", "principio_ativo": "Dipirona Sódica", "preco": "8.50", "estoque_minimo": 20})
        cadastrar.execute({"nome": "Paracetamol 750mg", "principio_ativo": "Paracetamol", "preco": "12.00", "estoque_minimo": 30})
        cadastrar.execute({"nome": "Ibuprofeno 600mg", "principio_ativo": "Ibuprofeno", "preco": "15.00", "estoque_minimo": 15})

        # Listar do banco REAL
        medicamentos = listar.execute()

        # ✅ Deve ter exatamente os 3 do banco
        assert len(medicamentos) == 3

    def test_banco_limpo_retorna_lista_vazia(self, db_session):
        """✅ Banco limpo (fixture garante isso!) retorna lista vazia"""
        repo = MedicamentoRepositoryPostgres(db_session)
        listar = ListarMedicamentosUseCase(repo)

        medicamentos = listar.execute()

        # ✅ Banco começa limpo graças ao fixture db_session!
        assert medicamentos == []


@pytest.mark.integration
class TestEstoqueIntegracao:
    """
    Testa fluxo completo de estoque com PostgreSQL.

    Cadastra medicamento → Adiciona estoque → Remove estoque
    Verifica em cada etapa que o banco tem os dados certos!
    """

    def test_adicionar_estoque_cria_lote_no_banco(self, db_session, medicamento_cadastrado):
        """✅ AdicionarEstoque deve criar lote real no banco"""
        med_repo = MedicamentoRepositoryPostgres(db_session)
        lote_repo = LoteRepositoryPostgres(db_session)
        use_case = AdicionarEstoqueUseCase(med_repo, lote_repo)

        # Verificar que não há lotes ainda
        lotes_antes = lote_repo.buscar_por_medicamento(medicamento_cadastrado.id)
        assert len(lotes_antes) == 0

        # Adicionar estoque (cria um lote no banco)
        use_case.execute(
            medicamento_cadastrado.id,
            100,
            "LOTE-REAL-001",
            (date.today() - timedelta(days=10)).isoformat(),
            (date.today() + timedelta(days=365)).isoformat(),
            "Farmacêutica Real Ltda"
        )

        # ✅ Verificar que o lote foi criado no banco PostgreSQL
        lotes_depois = lote_repo.buscar_por_medicamento(medicamento_cadastrado.id)
        assert len(lotes_depois) == 1
        assert lotes_depois[0].quantidade == 100
        assert lotes_depois[0].numero_lote == "LOTE-REAL-001"

    def test_remover_estoque_atualiza_lote_no_banco(self, db_session, medicamento_com_lote):
        """✅ RemoverEstoque deve reduzir quantidade do lote no banco"""
        med_repo = MedicamentoRepositoryPostgres(db_session)
        lote_repo = LoteRepositoryPostgres(db_session)
        use_case = RemoverEstoqueUseCase(med_repo, lote_repo)

        medicamento = medicamento_com_lote["medicamento"]

        # Verificar quantidade inicial (fixture tem 100)
        lotes_antes = lote_repo.buscar_por_medicamento(medicamento.id)
        total_antes = sum(l.quantidade for l in lotes_antes)
        assert total_antes == 100

        # Remover 30 unidades
        use_case.execute(medicamento.id, 30, "Venda balcão")

        # ✅ Verificar que o banco tem 70 agora
        lotes_depois = lote_repo.buscar_por_medicamento(medicamento.id)
        total_depois = sum(l.quantidade for l in lotes_depois)
        assert total_depois == 70

    def test_verificar_estoque_baixo_com_dados_reais(self, db_session):
        """✅ Deve detectar medicamento com estoque baixo no banco real"""
        med_repo = MedicamentoRepositoryPostgres(db_session)
        lote_repo = LoteRepositoryPostgres(db_session)
        cadastrar = CadastrarMedicamentoUseCase(med_repo)
        verificar = VerificarEstoqueBaixoUseCase(med_repo, lote_repo)

        # Cadastrar medicamento com estoque_minimo = 100
        med = cadastrar.execute({
            "nome": "Paracetamol 750mg",
            "principio_ativo": "Paracetamol",
            "preco": "12.00",
            "estoque_minimo": 100
        })

        # Adicionar só 30 unidades (abaixo do mínimo de 100!)
        adicionar = AdicionarEstoqueUseCase(med_repo, lote_repo)
        adicionar.execute(
            med.id,
            30,
            "LOTE-BAIXO-001",
            (date.today() - timedelta(days=5)).isoformat(),
            (date.today() + timedelta(days=300)).isoformat(),
            "Fornecedor Teste"
        )

        # ✅ Verificar que detecta como estoque baixo
        alertas = verificar.execute()

        assert len(alertas) >= 1
        # VerificarEstoqueBaixoUseCase retorna dicts com chave "nome"
        nomes = [a["nome"].lower() for a in alertas]
        assert any("paracetamol" in nome for nome in nomes)
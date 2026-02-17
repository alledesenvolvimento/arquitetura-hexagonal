"""
conftest.py — Fixtures de Integração

Configura banco de testes PostgreSQL para os testes de integração.
Cada teste roda com banco limpo e isolado!

Aula 14 - Testes de Integração
"""

import os
import pytest
from datetime import date, timedelta
from decimal import Decimal
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Carregar .env antes de tudo
load_dotenv()

# ======================================================
# CONFIGURAÇÃO DO BANCO DE TESTES
# ======================================================

# URL do banco de TESTES — separado do banco de produção!
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/allefarma_test"
)

# Criar engine apontando pro banco de TESTES
test_engine = create_engine(TEST_DATABASE_URL, echo=False)

# Criar fábrica de sessões de teste
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# ======================================================
# FIXTURES DE BANCO DE DADOS
# ======================================================

@pytest.fixture(scope="session")
def setup_banco_testes():
    """
    Fixture de sessão: roda UMA VEZ antes de todos os testes.

    Cria todas as tabelas no banco de testes.
    Depois de todos os testes, apaga tudo.

    scope="session" = roda só uma vez por execução do pytest!
    """
    from src.infrastructure.database.base import Base

    # Criar todas as tabelas no banco de TESTES
    Base.metadata.create_all(bind=test_engine)

    print("\n✅ Banco de testes configurado!")

    yield  # aqui os testes rodam

    # Depois de todos os testes: limpar tabelas
    Base.metadata.drop_all(bind=test_engine)
    print("\n🗑️ Banco de testes limpo!")


@pytest.fixture
def db_session(setup_banco_testes):
    """
    Fixture: sessão de banco para cada teste.

    Cria uma sessão, passa pro teste, faz ROLLBACK no final.
    Isso garante que cada teste começa com banco limpo! 🧹

    ROLLBACK = desfaz tudo que o teste fez no banco.
    """
    session = TestSessionLocal()

    # Limpar tabelas antes de cada teste
    # (garante banco limpo independente de ordem)
    _limpar_tabelas(session)

    try:
        yield session  # aqui o teste usa a sessão
    finally:
        session.rollback()  # desfaz qualquer coisa pendente
        session.close()     # fecha a sessão


def _limpar_tabelas(session):
    """
    Limpa todas as tabelas na ordem correta.

    Ordem importa por causa das foreign keys!
    Sempre apague as tabelas filhas antes das mães.
    """
    try:
        # Lotes antes de Medicamentos (foreign key!)
        session.execute(text("DELETE FROM lotes"))
        session.execute(text("DELETE FROM medicamentos"))
        session.commit()
    except Exception:
        session.rollback()


# ======================================================
# FIXTURE DO TESTCLIENT (API)
# ======================================================

@pytest.fixture
def client(db_session):
    """
    Fixture: TestClient do FastAPI configurado com banco de testes.

    Substitui a sessão de banco da aplicação pela sessão de testes!
    Assim a API usa o banco de TESTES, não o de produção. 🔒
    """
    from src.api.main import app
    from src.infrastructure.database.base import get_session

    # Substituir a dependência de banco pelo banco de TESTES
    def override_get_session():
        try:
            yield db_session
        finally:
            pass  # sessão já é gerenciada pelo fixture db_session

    # Registrar o override
    app.dependency_overrides[get_session] = override_get_session

    # Criar cliente de teste
    with TestClient(app) as test_client:
        yield test_client

    # Remover override após o teste
    app.dependency_overrides.clear()


# ======================================================
# FIXTURES DE DADOS
# ======================================================

@pytest.fixture
def medicamento_cadastrado(db_session):
    """
    Fixture: Dipirona já cadastrada no banco de testes.

    Útil para testes que precisam de um medicamento existente!
    """
    from src.adapters.repositories import MedicamentoRepositoryPostgres
    from src.application.use_cases import CadastrarMedicamentoUseCase

    repo = MedicamentoRepositoryPostgres(db_session)
    use_case = CadastrarMedicamentoUseCase(repo)

    medicamento = use_case.execute({
        "nome": "Dipirona 500mg",
        "principio_ativo": "Dipirona Sódica",
        "preco": "8.50",
        "estoque_minimo": 20,
        "requer_receita": False
    })

    db_session.commit()
    return medicamento


@pytest.fixture
def medicamento_com_lote(db_session, medicamento_cadastrado):
    """
    Fixture: medicamento com lote cadastrado no banco.

    Combina medicamento + lote para testes de estoque!
    """
    from src.adapters.repositories import LoteRepositoryPostgres
    from src.domain.entities import Lote

    lote_repo = LoteRepositoryPostgres(db_session)

    lote = Lote(
        numero_lote="LOTE-INT-001",
        medicamento_id=medicamento_cadastrado.id,
        quantidade=100,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica Teste Ltda"
    )

    lote_salvo = lote_repo.salvar(lote)
    db_session.commit()

    return {
        "medicamento": medicamento_cadastrado,
        "lote": lote_salvo
    }
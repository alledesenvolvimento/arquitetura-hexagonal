"""
Testes Parametrizados com @pytest.mark.parametrize

Um código de teste, vários cenários!
Evita repetição de código e torna os testes mais completos.

Aula 15 - Mocking e Fixtures
"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from unittest.mock import MagicMock

from src.domain.entities import Medicamento, Lote
from src.application.use_cases import (
    CadastrarMedicamentoUseCase,
    ListarMedicamentosUseCase,
)


# ============================================================
# TESTES PARAMETRIZADOS: Validações de Medicamento
# ============================================================

@pytest.mark.unit
class TestMedicamentoParametrizado:
    """
    Testes parametrizados para validações do Medicamento.

    Cada @parametrize roda o teste com uma lista de valores diferentes!
    """

    @pytest.mark.parametrize("nome_invalido, descricao", [
        ("",   "nome vazio"),
        ("  ", "nome só com espaços"),
        ("A",  "nome muito curto"),
    ])
    def test_nome_invalido_levanta_erro(self, nome_invalido, descricao):
        """
        ✅ Nomes inválidos devem lançar ValueError.

        Esse teste roda 4 vezes, uma pra cada nome!
        Sem parametrize, precisaríamos de 4 funções separadas. 😴
        """
        with pytest.raises(ValueError):
            Medicamento(
                nome=nome_invalido,
                principio_ativo="Dipirona Sódica",
                preco=Decimal("8.50"),
                estoque_atual=100,
                estoque_minimo=20,
                requer_receita=False,
            )

    @pytest.mark.parametrize("preco_invalido, descricao", [
        (Decimal("-1.00"),  "preço negativo"),
        (Decimal("0.00"),   "preço zero"),
        (Decimal("-0.01"),  "preço quase zero negativo"),
    ])
    def test_preco_invalido_levanta_erro(self, preco_invalido, descricao):
        """
        ✅ Preços inválidos (negativos ou zero) devem lançar ValueError.

        Roda 3 vezes, uma pra cada preço inválido!
        """
        with pytest.raises(ValueError):
            Medicamento(
                nome="Dipirona 500mg",
                principio_ativo="Dipirona Sódica",
                preco=preco_invalido,
                estoque_atual=100,
                estoque_minimo=20,
                requer_receita=False,
            )

    @pytest.mark.parametrize("preco_valido, descricao", [
        (Decimal("0.01"),    "preço mínimo"),
        (Decimal("8.50"),    "preço normal"),
        (Decimal("999.99"),  "preço alto"),
        (Decimal("1500.00"), "preço muito alto"),
    ])
    def test_preco_valido_aceito(self, preco_valido, descricao):
        """
        ✅ Preços válidos devem ser aceitos sem erro.

        Roda 4 vezes com preços diferentes!
        """
        med = Medicamento(
            nome="Dipirona 500mg",
            principio_ativo="Dipirona Sódica",
            preco=preco_valido,
            estoque_atual=100,
            estoque_minimo=20,
            requer_receita=False,
        )
        assert med.preco == preco_valido

    @pytest.mark.parametrize("estoque_atual, estoque_minimo, esperado_baixo", [
        (5,   10,  True),   # 5 < 10 → estoque baixo!
        (10,  10,  False),  # 10 == 10 → OK (no limite)
        (100, 20,  False),  # 100 > 20 → OK
        (0,   10,  True),   # 0 < 10 → estoque baixo!
        (1,   100, True),   # 1 < 100 → estoque baixo!
    ])
    def test_estoque_baixo_varios_cenarios(
        self, estoque_atual, estoque_minimo, esperado_baixo
    ):
        """
        ✅ Verifica estoque_baixo() com vários cenários.

        5 cenários diferentes, 1 código de teste!
        """
        med = Medicamento(
            nome="Dipirona 500mg",
            principio_ativo="Dipirona Sódica",
            preco=Decimal("8.50"),
            estoque_atual=estoque_atual,
            estoque_minimo=estoque_minimo,
            requer_receita=False,
        )
        assert med.estoque_baixo() == esperado_baixo


# ============================================================
# TESTES PARAMETRIZADOS: Validações de Lote
# ============================================================

@pytest.mark.unit
class TestLoteParametrizado:
    """
    Testes parametrizados para validações do Lote.
    """

    @pytest.mark.parametrize("quantidade_invalida, descricao", [
        (0,    "quantidade zero"),
        (-1,   "quantidade negativa"),
        (-100, "quantidade muito negativa"),
    ])
    def test_quantidade_invalida_levanta_erro(self, quantidade_invalida, descricao):
        """
        ✅ Quantidades inválidas devem lançar ValueError.

        Roda 3 vezes com quantidades inválidas!
        """
        with pytest.raises(ValueError):
            Lote(
                numero_lote="LOTE-123",
                medicamento_id=1,
                quantidade=quantidade_invalida,
                data_fabricacao=date.today() - timedelta(days=30),
                data_validade=date.today() + timedelta(days=365),
                fornecedor="Farmacêutica ABC",
            )

    @pytest.mark.parametrize("dias_futuros, dias_limite, esperado_breve", [
        (5,   30, True),   # vence em 5 dias, limite 30 → em breve!
        (15,  30, True),   # vence em 15 dias, limite 30 → em breve!
        (30,  30, True),   # vence em 30 dias, limite 30 → no limite!
        (31,  30, False),  # vence em 31 dias, limite 30 → ainda não
        (365, 30, False),  # vence em 1 ano → não urgente
    ])
    def test_vence_em_breve_varios_cenarios(
        self, dias_futuros, dias_limite, esperado_breve
    ):
        """
        ✅ Verifica vence_em_breve() com vários prazos.

        5 cenários em 1 teste!
        """
        lote = Lote(
            numero_lote="LOTE-PARAM-001",
            medicamento_id=1,
            quantidade=100,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=dias_futuros),
            fornecedor="Farmacêutica ABC",
        )
        assert lote.vence_em_breve(dias_limite) == esperado_breve


# ============================================================
# TESTES USANDO FIXTURES DE COMPOSIÇÃO DO CONFTEST
# ============================================================

@pytest.mark.unit
class TestFixturasComposicao:
    """
    Demonstra o uso das fixtures de composição adicionadas
    no conftest.py da Aula 15.

    As fixtures 'use_case_cadastrar', 'use_case_listar', etc.
    injetam o use case já configurado — não precisa criar manualmente!
    """

    def test_cadastrar_via_fixture_composicao(self, use_case_cadastrar):
        """
        ✅ Use case de cadastro injetado via fixture de composição.

        'use_case_cadastrar' já vem com o repositório configurado!
        """
        resultado = use_case_cadastrar.execute({
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 20,
            "requer_receita": False,
        })

        # ⚠️ A Factory aplica .title() no nome:
        # "Dipirona 500mg" → "Dipirona 500Mg"
        # Por isso verificamos com .lower() para não depender do case!
        assert "dipirona" in resultado.nome.lower()

    def test_listar_via_fixture_composicao(
        self, use_case_cadastrar, use_case_listar
    ):
        """
        ✅ Duas fixtures de composição trabalhando juntas!

        Ambas usam 'repositorio_medicamentos' do mesmo fixture,
        então os dados ficam compartilhados entre elas!
        """
        # Cadastrar via fixture de composição
        use_case_cadastrar.execute({
            "nome": "Paracetamol 750mg",
            "principio_ativo": "Paracetamol",
            "preco": "12.00",
            "estoque_minimo": 30,
        })

        # Listar via outra fixture de composição (mesmo repositório!)
        resultado = use_case_listar.execute()

        assert len(resultado) == 1
        assert "paracetamol" in resultado[0].nome.lower()

    def test_mock_via_fixture_reutilizavel(self, repo_medicamentos_mock):
        """
        ✅ Fixture de mock reutilizável do conftest.

        'repo_medicamentos_mock' é um MagicMock limpo!
        Você configura o comportamento no próprio teste.
        """
        # Configurar comportamento específico pra este teste
        repo_medicamentos_mock.listar_todos.return_value = []

        use_case = ListarMedicamentosUseCase(repo_medicamentos_mock)
        resultado = use_case.execute()

        assert resultado == []
        repo_medicamentos_mock.listar_todos.assert_called_once()

    def test_mocks_prontos_fixture(self, mocks_prontos):
        """
        ✅ Fixture 'mocks_prontos' com dados padrão configurados.

        Todos os mocks já vêm configurados — só usar!
        """
        use_case = ListarMedicamentosUseCase(mocks_prontos["repo_med"])
        resultado = use_case.execute()

        # O mock já foi configurado pra retornar 1 medicamento
        assert len(resultado) == 1
        assert "dipirona" in resultado[0].nome.lower()

    def test_yield_fixture_setup_teardown(self, repositorio_com_log):
        """
        ✅ Fixture com yield — setup e teardown automáticos!

        'repositorio_com_log' cria o repositório (setup) antes do teste
        e libera tudo (teardown) depois — automaticamente!
        """
        # O repositório já vem criado e vazio!
        assert repositorio_com_log is not None
        assert len(repositorio_com_log.listar_todos()) == 0

        # Salvar algo
        med = Medicamento(
            nome="Dipirona 500mg",
            principio_ativo="Dipirona Sódica",
            preco=Decimal("8.50"),
            estoque_atual=100,
            estoque_minimo=20,
            requer_receita=False,
        )
        repositorio_com_log.salvar(med)

        assert len(repositorio_com_log.listar_todos()) == 1

        # Quando o teste terminar, o teardown roda automaticamente!
        # (o print do TEARDOWN vai aparecer no terminal com -s)
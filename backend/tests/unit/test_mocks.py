"""
Testes com Mocks — unittest.mock

Testa use cases usando MagicMock como repositório falso.
Não precisa de banco de dados nem repositório em memória!

Aula 15 - Mocking e Fixtures
"""

import pytest
from decimal import Decimal
from datetime import date, timedelta
from unittest.mock import MagicMock, call

from src.domain.entities import Medicamento, Lote
from src.application.use_cases import (
    CadastrarMedicamentoUseCase,
    ListarMedicamentosUseCase,
    AdicionarEstoqueUseCase,
    VerificarEstoqueBaixoUseCase,
)


# ============================================================
# HELPERS — dados reutilizáveis nos testes
# ============================================================

def _criar_medicamento_fake(nome="Dipirona 500mg", requer_receita=False):
    """Cria um Medicamento fake para usar nos testes com mock."""
    return Medicamento(
        nome=nome,
        principio_ativo="Dipirona Sódica",
        preco=Decimal("8.50"),
        estoque_atual=100,
        estoque_minimo=20,
        requer_receita=requer_receita,
    )


def _criar_lote_fake(medicamento_id=1):
    """Cria um Lote fake para usar nos testes com mock."""
    return Lote(
        numero_lote="LOTE-MOCK-001",
        medicamento_id=medicamento_id,
        quantidade=100,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica Mock Ltda",
    )


# ============================================================
# TESTES: CadastrarMedicamentoUseCase com Mock
# ============================================================

@pytest.mark.unit
class TestCadastrarMedicamentoComMock:
    """
    Testa CadastrarMedicamentoUseCase usando MagicMock como repositório.

    Aqui a gente verifica não só o resultado, mas TAMBÉM
    se o repositório foi chamado do jeito certo!
    """

    def test_cadastrar_chama_salvar_uma_vez(self):
        """
        ✅ O use case deve chamar repo.salvar() exatamente 1 vez.

        Isso é algo que o repositório em memória não consegue verificar
        facilmente — mas o mock consegue!
        """
        # ARRANGE: criar mock do repositório
        repo_mock = MagicMock()

        # Definir o que repo.salvar() vai retornar
        medicamento_fake = _criar_medicamento_fake()
        repo_mock.salvar.return_value = medicamento_fake

        use_case = CadastrarMedicamentoUseCase(repo_mock)

        dados = {
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 20,
            "requer_receita": False,
        }

        # ACT: executar o use case
        resultado = use_case.execute(dados)

        # ASSERT: o resultado veio do mock
        assert resultado.nome == "Dipirona 500mg"

        # 🎯 ASSERT ESPECIAL: verificar a chamada ao repositório!
        repo_mock.salvar.assert_called_once()  # ← foi chamado exatamente 1 vez!

    def test_cadastrar_retorna_o_que_salvar_retornou(self):
        """
        ✅ O use case deve retornar exatamente o que repo.salvar() retornou.

        Isso testa se o use case não está "perdendo" o retorno do repositório!
        """
        # ARRANGE
        repo_mock = MagicMock()
        medicamento_fake = _criar_medicamento_fake(nome="Paracetamol 750mg")
        repo_mock.salvar.return_value = medicamento_fake

        use_case = CadastrarMedicamentoUseCase(repo_mock)

        # ACT
        resultado = use_case.execute({
            "nome": "Paracetamol 750mg",
            "principio_ativo": "Paracetamol",
            "preco": "12.00",
            "estoque_minimo": 30,
        })

        # ASSERT: resultado é EXATAMENTE o que o mock retornou
        assert resultado is medicamento_fake  # ← mesma referência!

    def test_cadastrar_nao_chama_listar(self):
        """
        ✅ Cadastrar medicamento NÃO deve chamar listar_todos.

        Verifica que o use case não faz chamadas desnecessárias ao banco!
        """
        # ARRANGE
        repo_mock = MagicMock()
        repo_mock.salvar.return_value = _criar_medicamento_fake()

        use_case = CadastrarMedicamentoUseCase(repo_mock)

        # ACT
        use_case.execute({
            "nome": "Rivotril 2mg",
            "principio_ativo": "Clonazepam",
            "preco": "45.90",
            "estoque_minimo": 10,
            "requer_receita": True,
        })

        # ASSERT: listar_todos NÃO foi chamado!
        repo_mock.listar_todos.assert_not_called()

    def test_cadastrar_propaga_erro_do_repositorio(self):
        """
        ✅ Se repo.salvar() lançar erro, o use case deve propagar.

        Usa side_effect para simular o repositório quebrando!
        """
        # ARRANGE: simular erro no repositório (banco caiu!)
        repo_mock = MagicMock()
        repo_mock.salvar.side_effect = Exception("Banco indisponível!")

        use_case = CadastrarMedicamentoUseCase(repo_mock)

        # ACT + ASSERT: o erro deve ser propagado
        with pytest.raises(Exception, match="Banco indisponível!"):
            use_case.execute({
                "nome": "Dipirona 500mg",
                "principio_ativo": "Dipirona Sódica",
                "preco": "8.50",
                "estoque_minimo": 20,
            })


# ============================================================
# TESTES: ListarMedicamentosUseCase com Mock
# ============================================================

@pytest.mark.unit
class TestListarMedicamentosComMock:
    """
    Testa ListarMedicamentosUseCase usando MagicMock.
    """

    def test_listar_retorna_lista_do_repositorio(self):
        """✅ O use case deve retornar o que repo.listar_todos() retornou."""
        # ARRANGE
        repo_mock = MagicMock()
        medicamentos_fake = [
            _criar_medicamento_fake(nome="Dipirona 500mg"),
            _criar_medicamento_fake(nome="Paracetamol 750mg"),
            _criar_medicamento_fake(nome="Rivotril 2mg"),
        ]
        repo_mock.listar_todos.return_value = medicamentos_fake

        use_case = ListarMedicamentosUseCase(repo_mock)

        # ACT
        resultado = use_case.execute()

        # ASSERT
        assert len(resultado) == 3
        repo_mock.listar_todos.assert_called_once()

    def test_listar_retorna_lista_vazia_quando_sem_medicamentos(self):
        """✅ Repositório vazio → use case retorna lista vazia."""
        # ARRANGE
        repo_mock = MagicMock()
        repo_mock.listar_todos.return_value = []

        use_case = ListarMedicamentosUseCase(repo_mock)

        # ACT
        resultado = use_case.execute()

        # ASSERT
        assert resultado == []
        repo_mock.listar_todos.assert_called_once()

    def test_listar_nao_chama_salvar(self):
        """✅ Listar NÃO deve modificar o repositório (não chama salvar)."""
        # ARRANGE
        repo_mock = MagicMock()
        repo_mock.listar_todos.return_value = []

        use_case = ListarMedicamentosUseCase(repo_mock)

        # ACT
        use_case.execute()

        # ASSERT: salvar não foi chamado (listar é operação de leitura!)
        repo_mock.salvar.assert_not_called()

    def test_listar_chama_listar_todos_com_call_count(self):
        """
        ✅ call_count verifica quantas vezes listar_todos foi chamado.

        Útil para garantir que o código não faz consultas desnecessárias!
        """
        # ARRANGE
        repo_mock = MagicMock()
        repo_mock.listar_todos.return_value = [_criar_medicamento_fake()]

        use_case = ListarMedicamentosUseCase(repo_mock)

        # ACT: chamar 3 vezes
        use_case.execute()
        use_case.execute()
        use_case.execute()

        # ASSERT: listar_todos foi chamado exatamente 3 vezes
        assert repo_mock.listar_todos.call_count == 3


# ============================================================
# TESTES: AdicionarEstoqueUseCase com Mock
# ============================================================

@pytest.mark.unit
class TestAdicionarEstoqueComMock:
    """
    Testa AdicionarEstoqueUseCase usando MagicMock.

    Aqui usamos DOIS repositórios mockados (medicamentos e lotes)!
    """

    def test_adicionar_estoque_chama_buscar_por_id(self):
        """
        ✅ O use case deve buscar o medicamento antes de adicionar o lote.

        Verifica que o use case valida se o medicamento existe!
        """
        # ARRANGE: dois mocks separados!
        repo_med_mock = MagicMock()
        repo_lotes_mock = MagicMock()

        medicamento_fake = _criar_medicamento_fake()
        lote_fake = _criar_lote_fake(medicamento_id=1)

        repo_med_mock.buscar_por_id.return_value = medicamento_fake
        repo_lotes_mock.salvar.return_value = lote_fake

        use_case = AdicionarEstoqueUseCase(repo_med_mock, repo_lotes_mock)

        # ACT: argumentos posicionais (igual ao test_use_cases.py da Aula 13!)
        use_case.execute(
            1,                                                        # medicamento_id
            100,                                                      # quantidade
            "LOTE-MOCK-001",                                          # numero_lote
            (date.today() - timedelta(days=30)).isoformat(),          # data_fabricacao
            (date.today() + timedelta(days=365)).isoformat(),         # data_validade
            "Farmacêutica Mock Ltda",                                 # fornecedor
        )

        # ASSERT: verificar que buscou o medicamento antes de salvar o lote
        repo_med_mock.buscar_por_id.assert_called_once_with(1)

    def test_adicionar_estoque_chama_salvar_no_repo_lotes(self):
        """
        ✅ O use case deve salvar o lote no repositório de lotes.
        """
        # ARRANGE
        repo_med_mock = MagicMock()
        repo_lotes_mock = MagicMock()

        medicamento_fake = _criar_medicamento_fake()
        lote_fake = _criar_lote_fake(medicamento_id=1)

        repo_med_mock.buscar_por_id.return_value = medicamento_fake
        repo_lotes_mock.salvar.return_value = lote_fake

        use_case = AdicionarEstoqueUseCase(repo_med_mock, repo_lotes_mock)

        # ACT: argumentos posicionais (igual ao test_use_cases.py da Aula 13!)
        use_case.execute(
            1,                                                        # medicamento_id
            100,                                                      # quantidade
            "LOTE-MOCK-001",                                          # numero_lote
            (date.today() - timedelta(days=30)).isoformat(),          # data_fabricacao
            (date.today() + timedelta(days=365)).isoformat(),         # data_validade
            "Farmacêutica Mock Ltda",                                 # fornecedor
        )

        # ASSERT: o lote foi salvo no repositório de lotes
        repo_lotes_mock.salvar.assert_called_once()

    def test_adicionar_estoque_falha_se_medicamento_nao_existe(self):
        """
        ✅ Deve lançar erro se o medicamento não existir.

        Usa return_value=None para simular medicamento não encontrado!
        """
        # ARRANGE: medicamento não encontrado
        repo_med_mock = MagicMock()
        repo_lotes_mock = MagicMock()

        repo_med_mock.buscar_por_id.return_value = None  # ← não existe!

        use_case = AdicionarEstoqueUseCase(repo_med_mock, repo_lotes_mock)

        # ACT + ASSERT: deve lançar erro de medicamento não encontrado
        with pytest.raises((ValueError, Exception)):
            use_case.execute(
                999,                                                      # medicamento_id que não existe
                100,                                                      # quantidade
                "LOTE-X",                                                 # numero_lote
                (date.today() - timedelta(days=30)).isoformat(),          # data_fabricacao
                (date.today() + timedelta(days=365)).isoformat(),         # data_validade
                "Fornecedor X",                                           # fornecedor
            )

        # ASSERT EXTRA: o repositório de lotes NÃO deve ter sido chamado!
        repo_lotes_mock.salvar.assert_not_called()


# ============================================================
# TESTES: side_effect — simulando erros e sequências
# ============================================================

@pytest.mark.unit
class TestSideEffect:
    """
    Testa o poder do side_effect para simular erros e sequências.
    """

    def test_side_effect_simula_banco_indisponivel(self):
        """
        ✅ side_effect pode simular qualquer exceção.

        Isso testa como o código se comporta quando o banco cai!
        É impossível fazer esse teste com repositório em memória.
        """
        # ARRANGE: banco vai "cair" na hora de salvar
        repo_mock = MagicMock()
        repo_mock.salvar.side_effect = ConnectionError("Banco PostgreSQL caiu!")

        use_case = CadastrarMedicamentoUseCase(repo_mock)

        # ACT + ASSERT
        with pytest.raises((ConnectionError, Exception)):
            use_case.execute({
                "nome": "Dipirona 500mg",
                "principio_ativo": "Dipirona Sódica",
                "preco": "8.50",
                "estoque_minimo": 20,
            })

    def test_side_effect_sequencia_de_retornos(self):
        """
        ✅ side_effect com lista retorna valores diferentes a cada chamada.

        Útil para simular: 1ª chamada retorna A, 2ª retorna B, 3ª retorna C.
        """
        # ARRANGE: cada chamada retorna um medicamento diferente
        repo_mock = MagicMock()

        med1 = _criar_medicamento_fake(nome="Dipirona 500mg")
        med2 = _criar_medicamento_fake(nome="Paracetamol 750mg")

        # Lista: 1ª chamada → med1, 2ª → med2, 3ª → None
        repo_mock.buscar_por_id.side_effect = [med1, med2, None]

        # ACT + ASSERT: cada chamada retorna o próximo da lista
        resultado1 = repo_mock.buscar_por_id(1)
        resultado2 = repo_mock.buscar_por_id(2)
        resultado3 = repo_mock.buscar_por_id(99)

        assert resultado1.nome == "Dipirona 500mg"
        assert resultado2.nome == "Paracetamol 750mg"
        assert resultado3 is None

    def test_side_effect_diferentes_chamadas_salvar(self):
        """
        ✅ Verificar chamadas diferentes ao mesmo método.

        Simula: 1ª vez funciona, 2ª vez falha (timeout intermitente).
        """
        # ARRANGE
        repo_mock = MagicMock()
        medicamento_fake = _criar_medicamento_fake()

        # 1ª chamada funciona, 2ª falha
        repo_mock.salvar.side_effect = [
            medicamento_fake,
            ConnectionError("Timeout na 2ª tentativa!"),
        ]

        use_case = CadastrarMedicamentoUseCase(repo_mock)
        dados = {
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": "8.50",
            "estoque_minimo": 20,
        }

        # ACT: primeira chamada funciona
        resultado = use_case.execute(dados)
        assert resultado is medicamento_fake

        # ACT + ASSERT: segunda chamada falha
        with pytest.raises((ConnectionError, Exception)):
            use_case.execute(dados)
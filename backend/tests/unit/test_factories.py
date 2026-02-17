"""
Testes Unitários: Factory Pattern
Testa MedicamentoFactory usando pytest

Aula 13 - Testes Unitários
"""

import pytest
from decimal import Decimal

from src.domain.factories import MedicamentoFactory


class TestMedicamentoFactory:
    """Testes para o Factory Pattern"""

    # --- Testes de Criação Básica ---

    def test_criar_medicamento_basico(self):
        """✅ Deve criar medicamento com valores básicos"""
        medicamento = MedicamentoFactory.criar(
            nome="dipirona",
            principio_ativo="dipirona sódica",
            preco=15.50
        )

        assert medicamento.nome == "Dipirona"  # padronizado com .title()!
        assert medicamento.principio_ativo == "Dipirona Sódica"
        assert medicamento.preco == Decimal("15.50")

    def test_criar_medicamento_aplica_estoque_minimo_padrao(self):
        """✅ Deve aplicar estoque mínimo padrão (50) quando não informado"""
        medicamento = MedicamentoFactory.criar(
            nome="Paracetamol",
            principio_ativo="Paracetamol",
            preco=10.00
        )

        assert medicamento.estoque_minimo == 50  # valor padrão!

    def test_criar_medicamento_com_estoque_minimo_customizado(self):
        """✅ Deve usar estoque mínimo personalizado quando informado"""
        medicamento = MedicamentoFactory.criar(
            nome="Rivotril",
            principio_ativo="Clonazepam",
            preco=45.90,
            estoque_minimo=100
        )

        assert medicamento.estoque_minimo == 100

    def test_criar_medicamento_controlado(self):
        """✅ Deve criar medicamento controlado (requer receita)"""
        medicamento = MedicamentoFactory.criar(
            nome="Rivotril 2mg",
            principio_ativo="Clonazepam",
            preco=45.90,
            controlado=True
        )

        assert medicamento.requer_receita is True

    def test_criar_medicamento_nao_controlado_por_padrao(self):
        """✅ Medicamentos não devem ser controlados por padrão"""
        medicamento = MedicamentoFactory.criar(
            nome="Dipirona",
            principio_ativo="Dipirona",
            preco=8.50
        )

        assert medicamento.requer_receita is False

    def test_padroniza_nome_com_title(self):
        """✅ Deve padronizar nome com title() (primeira letra maiúscula)"""
        medicamento = MedicamentoFactory.criar(
            nome="DIPIRONA SÓDICA 500MG",
            principio_ativo="dipirona",
            preco=8.50
        )

        # .title() transforma em "Dipirona Sódica 500Mg"
        assert medicamento.nome == "Dipirona Sódica 500Mg"

    # --- Testes de Validação ---

    def test_preco_zero_levanta_erro(self):
        """❌ Deve rejeitar preço zero"""
        with pytest.raises(ValueError):
            MedicamentoFactory.criar(
                nome="Teste",
                principio_ativo="Teste",
                preco=0
            )

    def test_preco_negativo_levanta_erro(self):
        """❌ Deve rejeitar preço negativo"""
        with pytest.raises(ValueError):
            MedicamentoFactory.criar(
                nome="Teste",
                principio_ativo="Teste",
                preco=-5.0
            )

    def test_nome_muito_curto_levanta_erro(self):
        """❌ Deve rejeitar nome com menos de 3 caracteres"""
        with pytest.raises(ValueError):
            MedicamentoFactory.criar(
                nome="AB",
                principio_ativo="Teste",
                preco=10.0
            )

    def test_nome_vazio_levanta_erro(self):
        """❌ Deve rejeitar nome vazio"""
        with pytest.raises(ValueError):
            MedicamentoFactory.criar(
                nome="",
                principio_ativo="Teste",
                preco=10.0
            )

    def test_principio_ativo_vazio_levanta_erro(self):
        """❌ Deve rejeitar princípio ativo vazio"""
        with pytest.raises(ValueError):
            MedicamentoFactory.criar(
                nome="Dipirona",
                principio_ativo="",
                preco=10.0
            )

    # --- Testes de Criação com Lote Inicial ---

    def test_criar_com_lote_inicial_retorna_tupla(self):
        """✅ Deve retornar tupla (medicamento, lote)"""
        resultado = MedicamentoFactory.criar_com_lote_inicial(
            nome="Paracetamol",
            principio_ativo="Paracetamol",
            preco=8.50,
            numero_lote="LOT123",
            quantidade_inicial=200,
            data_fabricacao="2026-01-01",
            data_validade="2027-01-01",
            fornecedor="farmasa"
        )

        assert isinstance(resultado, tuple)
        assert len(resultado) == 2

    def test_criar_com_lote_inicial_dados_corretos(self):
        """✅ Medicamento e lote devem ter dados corretos"""
        medicamento, lote = MedicamentoFactory.criar_com_lote_inicial(
            nome="Paracetamol",
            principio_ativo="Paracetamol",
            preco=8.50,
            numero_lote="LOT123",
            quantidade_inicial=200,
            data_fabricacao="2026-01-01",
            data_validade="2027-01-01",
            fornecedor="farmasa"
        )

        assert medicamento.nome == "Paracetamol"
        assert lote.numero_lote == "LOT123"
        assert lote.quantidade == 200
        assert lote.fornecedor == "Farmasa"  # padronizado com .title()!

    def test_criar_com_lote_inicial_vincula_medicamento_ao_lote(self):
        """✅ Lote deve estar vinculado ao medicamento criado"""
        medicamento, lote = MedicamentoFactory.criar_com_lote_inicial(
            nome="Dipirona",
            principio_ativo="Dipirona",
            preco=8.50,
            numero_lote="LOT-001",
            quantidade_inicial=100,
            data_fabricacao="2026-01-01",
            data_validade="2027-01-01",
            fornecedor="Farmacêutica"
        )

        assert lote.medicamento_id == medicamento.id

    def test_criar_com_lote_inicial_quantidade_zero_levanta_erro(self):
        """❌ Deve rejeitar quantidade inicial zero"""
        with pytest.raises(ValueError):
            MedicamentoFactory.criar_com_lote_inicial(
                nome="Dipirona",
                principio_ativo="Dipirona",
                preco=8.50,
                numero_lote="LOT-001",
                quantidade_inicial=0,  # inválido!
                data_fabricacao="2026-01-01",
                data_validade="2027-01-01",
                fornecedor="Farmacêutica"
            )
"""
Testes Unitários: Entidades do Domínio
Testa Medicamento e Lote usando pytest

Aula 13 - Testes Unitários
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from src.domain.entities import Medicamento, Lote


# ==========================================
# TESTES DA ENTIDADE MEDICAMENTO
# ==========================================

class TestMedicamento:
    """Grupo de testes para a entidade Medicamento"""

    # --- Testes de Criação ---

    def test_criar_medicamento_valido(self):
        """✅ Deve criar medicamento com dados válidos"""
        medicamento = Medicamento(
            nome="Dipirona 500mg",
            principio_ativo="Dipirona Sódica",
            preco=Decimal("8.50"),
            estoque_atual=100,
            estoque_minimo=20,
            requer_receita=False
        )

        assert medicamento.nome == "Dipirona 500mg"
        assert medicamento.principio_ativo == "Dipirona Sódica"
        assert medicamento.preco == Decimal("8.50")
        assert medicamento.estoque_atual == 100
        assert medicamento.estoque_minimo == 20
        assert medicamento.requer_receita is False

    def test_criar_medicamento_controlado(self):
        """✅ Deve criar medicamento controlado (requer receita)"""
        medicamento = Medicamento(
            nome="Rivotril 2mg",
            principio_ativo="Clonazepam",
            preco=Decimal("45.90"),
            estoque_atual=50,
            estoque_minimo=10,
            requer_receita=True
        )

        assert medicamento.requer_receita is True
        assert medicamento.requer_receita_medica() is True

    def test_criar_medicamento_sem_id(self):
        """✅ Deve criar medicamento sem ID (será gerado pelo banco)"""
        medicamento = Medicamento(
            nome="Ibuprofeno 600mg",
            principio_ativo="Ibuprofeno",
            preco=Decimal("15.50"),
            estoque_atual=0,
            estoque_minimo=5,
            requer_receita=False
        )

        assert medicamento.id is None

    # --- Testes de Validação de Nome ---

    def test_nome_vazio_levanta_erro(self):
        """❌ Deve rejeitar nome vazio"""
        with pytest.raises(ValueError, match="Nome do medicamento é obrigatório"):
            Medicamento(
                nome="",
                principio_ativo="Teste",
                preco=Decimal("10.00"),
                estoque_minimo=5
            )

    def test_nome_apenas_espacos_levanta_erro(self):
        """❌ Deve rejeitar nome com apenas espaços"""
        with pytest.raises(ValueError):
            Medicamento(
                nome="   ",
                principio_ativo="Teste",
                preco=Decimal("10.00"),
                estoque_minimo=5
            )

    def test_nome_muito_curto_levanta_erro(self):
        """❌ Deve rejeitar nome com menos de 3 caracteres"""
        with pytest.raises(ValueError, match="pelo menos 3 caracteres"):
            Medicamento(
                nome="AB",
                principio_ativo="Teste",
                preco=Decimal("10.00"),
                estoque_minimo=5
            )

    # --- Testes de Validação de Princípio Ativo ---

    def test_principio_ativo_vazio_levanta_erro(self):
        """❌ Deve rejeitar princípio ativo vazio"""
        with pytest.raises(ValueError, match="Princípio ativo é obrigatório"):
            Medicamento(
                nome="Teste Medicamento",
                principio_ativo="",
                preco=Decimal("10.00"),
                estoque_minimo=5
            )

    # --- Testes de Validação de Preço ---

    def test_preco_negativo_levanta_erro(self):
        """❌ Deve rejeitar preço negativo"""
        with pytest.raises(ValueError, match="Preço deve ser maior que zero"):
            Medicamento(
                nome="Teste Med",
                principio_ativo="Teste Ativo",
                preco=Decimal("-5.00"),
                estoque_minimo=5
            )

    def test_preco_zero_levanta_erro(self):
        """❌ Deve rejeitar preço igual a zero"""
        with pytest.raises(ValueError, match="Preço deve ser maior que zero"):
            Medicamento(
                nome="Teste Med",
                principio_ativo="Teste Ativo",
                preco=Decimal("0.00"),
                estoque_minimo=5
            )

    # --- Testes de Validação de Estoque ---

    def test_estoque_negativo_levanta_erro(self):
        """❌ Deve rejeitar estoque atual negativo"""
        with pytest.raises(ValueError, match="Estoque atual não pode ser negativo"):
            Medicamento(
                nome="Teste Med",
                principio_ativo="Teste Ativo",
                preco=Decimal("10.00"),
                estoque_atual=-1,
                estoque_minimo=5
            )

    def test_estoque_minimo_negativo_levanta_erro(self):
        """❌ Deve rejeitar estoque mínimo negativo"""
        with pytest.raises(ValueError, match="Estoque mínimo não pode ser negativo"):
            Medicamento(
                nome="Teste Med",
                principio_ativo="Teste Ativo",
                preco=Decimal("10.00"),
                estoque_atual=0,
                estoque_minimo=-5
            )

    # --- Testes de Validação de Validade ---

    def test_validade_vencida_levanta_erro(self):
        """❌ Deve rejeitar medicamento com validade vencida"""
        with pytest.raises(ValueError, match="validade vencida"):
            Medicamento(
                nome="Teste Med",
                principio_ativo="Teste Ativo",
                preco=Decimal("10.00"),
                estoque_minimo=5,
                data_validade=date.today() - timedelta(days=1)
            )

    def test_validade_hoje_levanta_erro(self):
        """❌ Deve rejeitar medicamento com validade vencendo hoje"""
        with pytest.raises(ValueError):
            Medicamento(
                nome="Teste Med",
                principio_ativo="Teste Ativo",
                preco=Decimal("10.00"),
                estoque_minimo=5,
                data_validade=date.today()
            )

    # --- Testes de Métodos de Negócio ---

    def test_estoque_baixo_retorna_true(self, medicamento_estoque_baixo):
        """✅ Deve retornar True quando estoque está abaixo do mínimo"""
        # estoque_atual=5, estoque_minimo=10 → 5 < 10 = baixo!
        assert medicamento_estoque_baixo.estoque_baixo() is True

    def test_estoque_baixo_retorna_false(self, medicamento_dipirona):
        """✅ Deve retornar False quando estoque está adequado"""
        # estoque_atual=100, estoque_minimo=20 → 100 > 20 = ok!
        assert medicamento_dipirona.estoque_baixo() is False

    def test_baixar_estoque_funciona(self, medicamento_dipirona):
        """✅ Deve reduzir estoque após venda"""
        estoque_inicial = medicamento_dipirona.estoque_atual  # 100
        medicamento_dipirona.baixar_estoque(30)

        assert medicamento_dipirona.estoque_atual == estoque_inicial - 30  # 70

    def test_baixar_estoque_insuficiente_levanta_erro(self, medicamento_dipirona):
        """❌ Deve rejeitar venda com estoque insuficiente"""
        with pytest.raises(ValueError, match="Estoque insuficiente"):
            medicamento_dipirona.baixar_estoque(999)  # só tem 100!

    def test_repor_estoque_funciona(self, medicamento_dipirona):
        """✅ Deve aumentar estoque após reposição"""
        estoque_inicial = medicamento_dipirona.estoque_atual  # 100
        medicamento_dipirona.repor_estoque(50)

        assert medicamento_dipirona.estoque_atual == estoque_inicial + 50  # 150

    def test_repor_estoque_zero_levanta_erro(self, medicamento_dipirona):
        """❌ Deve rejeitar reposição com quantidade zero"""
        with pytest.raises(ValueError):
            medicamento_dipirona.repor_estoque(0)

    def test_pode_vender_retorna_true(self, medicamento_dipirona):
        """✅ Deve permitir venda quando há estoque"""
        assert medicamento_dipirona.pode_vender(50) is True

    def test_medicamento_nao_controlado_nao_requer_receita(self, medicamento_dipirona):
        """✅ Medicamento comum não deve requerer receita"""
        assert medicamento_dipirona.requer_receita_medica() is False

    def test_medicamento_controlado_requer_receita(self, medicamento_controlado):
        """✅ Medicamento controlado deve requerer receita"""
        assert medicamento_controlado.requer_receita_medica() is True


# ==========================================
# TESTES DA ENTIDADE LOTE
# ==========================================

class TestLote:
    """Grupo de testes para a entidade Lote"""

    # --- Testes de Criação ---

    def test_criar_lote_valido(self):
        """✅ Deve criar lote com dados válidos"""
        lote = Lote(
            numero_lote="LOTE-2026-001",
            medicamento_id=1,
            quantidade=500,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Farmacêutica ABC Ltda"
        )

        assert lote.numero_lote == "LOTE-2026-001"
        assert lote.quantidade == 500
        assert lote.fornecedor == "Farmacêutica ABC Ltda"

    # --- Testes de Validação ---

    def test_numero_lote_vazio_levanta_erro(self):
        """❌ Deve rejeitar número de lote vazio"""
        with pytest.raises(ValueError, match="Número do lote é obrigatório"):
            Lote(
                numero_lote="",
                medicamento_id=1,
                quantidade=100,
                data_fabricacao=date.today() - timedelta(days=30),
                data_validade=date.today() + timedelta(days=365),
                fornecedor="Farmacêutica XYZ"
            )

    def test_quantidade_negativa_levanta_erro(self):
        """❌ Deve rejeitar quantidade negativa"""
        with pytest.raises(ValueError, match="maior que zero"):
            Lote(
                numero_lote="LOTE-123",
                medicamento_id=1,
                quantidade=-50,
                data_fabricacao=date.today() - timedelta(days=30),
                data_validade=date.today() + timedelta(days=365),
                fornecedor="Farmacêutica XYZ"
            )

    def test_quantidade_zero_levanta_erro(self):
        """❌ Deve rejeitar quantidade zero"""
        with pytest.raises(ValueError, match="maior que zero"):
            Lote(
                numero_lote="LOTE-123",
                medicamento_id=1,
                quantidade=0,
                data_fabricacao=date.today() - timedelta(days=30),
                data_validade=date.today() + timedelta(days=365),
                fornecedor="Farmacêutica XYZ"
            )

    def test_validade_antes_fabricacao_levanta_erro(self):
        """❌ Deve rejeitar validade anterior à fabricação"""
        with pytest.raises(ValueError, match="posterior à data de fabricação"):
            Lote(
                numero_lote="LOTE-123",
                medicamento_id=1,
                quantidade=100,
                data_fabricacao=date.today() - timedelta(days=10),
                data_validade=date.today() - timedelta(days=20),  # ← antes!
                fornecedor="Farmacêutica XYZ"
            )

    def test_fornecedor_vazio_levanta_erro(self):
        """❌ Deve rejeitar fornecedor vazio"""
        with pytest.raises(ValueError, match="Fornecedor é obrigatório"):
            Lote(
                numero_lote="LOTE-123",
                medicamento_id=1,
                quantidade=100,
                data_fabricacao=date.today() - timedelta(days=30),
                data_validade=date.today() + timedelta(days=365),
                fornecedor=""
            )

    # --- Testes de Métodos de Negócio ---

    def test_lote_nao_vencido(self, lote_valido):
        """✅ Lote válido não deve estar vencido"""
        assert lote_valido.esta_vencido() is False

    def test_dias_para_vencer_positivo(self, lote_valido):
        """✅ Lote válido deve ter dias positivos para vencer"""
        dias = lote_valido.dias_para_vencer()
        assert dias > 0

    def test_vence_em_breve_true(self, lote_vencendo_breve):
        """✅ Lote que vence em 15 dias deve ser 'em breve' para 30 dias"""
        # vence em 15 dias → dentro do prazo de 30 → True
        assert lote_vencendo_breve.vence_em_breve(30) is True

    def test_vence_em_breve_false(self, lote_vencendo_breve):
        """✅ Lote que vence em 15 dias NÃO é 'em breve' para 10 dias"""
        # vence em 15 dias → fora do prazo de 10 → False
        assert lote_vencendo_breve.vence_em_breve(10) is False

    def test_vence_em_breve_padrao_30_dias(self, lote_vencendo_breve):
        """✅ Padrão de 'em breve' é 30 dias"""
        assert lote_vencendo_breve.vence_em_breve() is True  # padrão=30

    def test_retirar_quantidade_funciona(self, lote_valido):
        """✅ Deve reduzir quantidade após retirada"""
        quantidade_inicial = lote_valido.quantidade  # 500
        lote_valido.retirar_quantidade(100)

        assert lote_valido.quantidade == quantidade_inicial - 100  # 400

    def test_retirar_mais_que_disponivel_levanta_erro(self, lote_valido):
        """❌ Deve rejeitar retirada maior que o disponível"""
        with pytest.raises(ValueError, match="Quantidade insuficiente"):
            lote_valido.retirar_quantidade(9999)  # só tem 500!

    def test_adicionar_quantidade_funciona(self, lote_valido):
        """✅ Deve aumentar quantidade após adição"""
        quantidade_inicial = lote_valido.quantidade  # 500
        lote_valido.adicionar_quantidade(50)

        assert lote_valido.quantidade == quantidade_inicial + 50  # 550
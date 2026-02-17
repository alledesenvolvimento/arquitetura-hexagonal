"""
Testes Unitários: Value Objects
Testa CPF, Telefone e Receita usando pytest

Aula 13 - Testes Unitários
"""

import pytest
from datetime import date, timedelta

from src.domain.value_objects import CPF, Telefone
from src.domain.value_objects.receita import Receita


# ==========================================
# TESTES DO VALUE OBJECT CPF
# ==========================================

class TestCPF:
    """Grupo de testes para o Value Object CPF"""

    # --- Testes de Criação ---

    def test_criar_cpf_valido_sem_formatacao(self):
        """✅ Deve criar CPF válido a partir de número sem formatação"""
        cpf = CPF("12345678909")

        assert cpf.numero == "123.456.789-09"  # formatado automaticamente!

    def test_criar_cpf_valido_com_formatacao(self):
        """✅ Deve criar CPF válido a partir de número formatado"""
        cpf = CPF("123.456.789-09")

        assert cpf.numero == "123.456.789-09"

    def test_cpf_sem_formatacao_retorna_so_numeros(self):
        """✅ sem_formatacao() deve retornar apenas dígitos"""
        cpf = CPF("123.456.789-09")

        assert cpf.sem_formatacao() == "12345678909"

    # --- Testes de Imutabilidade ---

    def test_cpf_e_imutavel(self):
        """✅ CPF é imutável (frozen=True) - não pode ser alterado"""
        cpf = CPF("12345678909")

        with pytest.raises(Exception):  # FrozenInstanceError
            cpf.numero = "999.999.999-99"

    # --- Testes de Igualdade ---

    def test_cpfs_iguais_com_mesma_formatacao(self):
        """✅ Dois CPFs com mesmo valor devem ser iguais"""
        cpf1 = CPF("123.456.789-09")
        cpf2 = CPF("123.456.789-09")

        assert cpf1 == cpf2

    def test_cpfs_iguais_formatacoes_diferentes(self):
        """✅ CPF com e sem formatação devem ser iguais (mesmo valor)"""
        cpf1 = CPF("123.456.789-09")
        cpf2 = CPF("12345678909")  # sem formatação

        assert cpf1 == cpf2

    # --- Testes de Validação ---

    def test_cpf_com_menos_digitos_levanta_erro(self):
        """❌ Deve rejeitar CPF com menos de 11 dígitos"""
        with pytest.raises(ValueError, match="11 dígitos"):
            CPF("123456789")  # apenas 9 dígitos!

    def test_cpf_com_mais_digitos_levanta_erro(self):
        """❌ Deve rejeitar CPF com mais de 11 dígitos"""
        with pytest.raises(ValueError, match="11 dígitos"):
            CPF("123456789012")  # 12 dígitos!

    def test_cpf_todos_digitos_iguais_levanta_erro(self):
        """❌ Deve rejeitar CPF com todos os dígitos iguais"""
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("111.111.111-11")

    def test_cpf_todos_zeros_levanta_erro(self):
        """❌ Deve rejeitar CPF 000.000.000-00"""
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("000.000.000-00")

    def test_cpf_digitos_verificadores_errados_levanta_erro(self):
        """❌ Deve rejeitar CPF com dígitos verificadores incorretos"""
        with pytest.raises(ValueError, match="dígitos verificadores"):
            CPF("123.456.789-00")  # dígitos errados!

    # --- Testes de Representação ---

    def test_str_retorna_cpf_formatado(self):
        """✅ str(cpf) deve retornar CPF formatado"""
        cpf = CPF("12345678909")

        assert str(cpf) == "123.456.789-09"


# ==========================================
# TESTES DO VALUE OBJECT TELEFONE
# ==========================================

class TestTelefone:
    """Grupo de testes para o Value Object Telefone"""

    # --- Testes de Criação ---

    def test_criar_celular_valido(self):
        """✅ Deve criar celular válido (11 dígitos)"""
        tel = Telefone("11987654321")

        assert tel.eh_celular() is True

    def test_criar_fixo_valido(self):
        """✅ Deve criar telefone fixo válido (10 dígitos)"""
        tel = Telefone("1133334444")

        assert tel.eh_celular() is False

    def test_criar_celular_formatado(self):
        """✅ Deve criar celular a partir de número formatado"""
        tel = Telefone("(11) 98765-4321")

        assert tel.eh_celular() is True

    def test_telefone_sem_formatacao(self):
        """✅ sem_formatacao() deve retornar apenas dígitos"""
        tel = Telefone("(11) 98765-4321")

        assert tel.sem_formatacao() == "11987654321"

    def test_ddd_extraido_corretamente(self):
        """✅ Deve extrair DDD corretamente"""
        tel = Telefone("11987654321")

        assert tel.ddd() == "11"

    def test_ddd_diferente(self):
        """✅ Deve extrair DDD de SP (11), RJ (21), etc."""
        tel_rj = Telefone("21987654321")
        tel_sp = Telefone("11987654321")

        assert tel_rj.ddd() == "21"
        assert tel_sp.ddd() == "11"

    # --- Testes de Imutabilidade ---

    def test_telefone_e_imutavel(self):
        """✅ Telefone é imutável (frozen=True)"""
        tel = Telefone("11987654321")

        with pytest.raises(Exception):  # FrozenInstanceError
            tel.numero = "(99) 99999-9999"

    # --- Testes de Igualdade ---

    def test_telefones_iguais_mesma_formatacao(self):
        """✅ Dois telefones com mesmo valor devem ser iguais"""
        tel1 = Telefone("11987654321")
        tel2 = Telefone("11987654321")

        assert tel1 == tel2

    def test_telefones_iguais_formatacoes_diferentes(self):
        """✅ Mesmo telefone com formatos diferentes deve ser igual"""
        tel1 = Telefone("(11) 98765-4321")
        tel2 = Telefone("11987654321")

        assert tel1 == tel2

    # --- Testes de Validação ---

    def test_telefone_muito_curto_levanta_erro(self):
        """❌ Deve rejeitar telefone com poucos dígitos"""
        with pytest.raises(ValueError):
            Telefone("1199999")  # menos de 10 dígitos!

    def test_telefone_muito_longo_levanta_erro(self):
        """❌ Deve rejeitar telefone com muitos dígitos"""
        with pytest.raises(ValueError):
            Telefone("119876543210")  # 12 dígitos!

    def test_ddd_invalido_levanta_erro(self):
        """❌ Deve rejeitar DDD inválido (abaixo de 11)"""
        with pytest.raises(ValueError, match="DDD inválido"):
            Telefone("0199999999")  # DDD 01 não existe!

    def test_celular_sem_nove_levanta_erro(self):
        """❌ Deve rejeitar celular que não começa com 9"""
        with pytest.raises(ValueError, match="Celular deve começar com 9"):
            Telefone("11887654321")  # começa com 8, não com 9!

    # --- Testes de Representação ---

    def test_str_retorna_telefone_formatado_celular(self):
        """✅ str(tel) deve retornar celular formatado (XX) XXXXX-XXXX"""
        tel = Telefone("11987654321")

        assert str(tel) == "(11) 98765-4321"

    def test_str_retorna_telefone_formatado_fixo(self):
        """✅ str(tel) deve retornar fixo formatado (XX) XXXX-XXXX"""
        tel = Telefone("1133334444")

        assert str(tel) == "(11) 3333-4444"
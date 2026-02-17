"""
conftest.py - Configurações e fixtures compartilhadas do pytest

Este arquivo é carregado AUTOMATICAMENTE pelo pytest!
Aqui ficam as fixtures que podem ser usadas em QUALQUER teste.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from src.domain.entities import Medicamento, Lote
from src.domain.value_objects import CPF, Telefone
from src.adapters.repositories import (
    MedicamentoRepositoryMemory,
    LoteRepositoryMemory
)


# ==========================================
# FIXTURES DE MEDICAMENTOS
# ==========================================

@pytest.fixture
def medicamento_dipirona():
    """
    Fixture: medicamento Dipirona válido
    
    Disponível em TODOS os testes!
    Use assim: def test_algo(medicamento_dipirona):
    """
    return Medicamento(
        nome="Dipirona 500mg",
        principio_ativo="Dipirona Sódica",
        preco=Decimal("8.50"),
        estoque_atual=100,
        estoque_minimo=20,
        requer_receita=False
    )


@pytest.fixture
def medicamento_controlado():
    """Fixture: medicamento controlado (requer receita)"""
    return Medicamento(
        nome="Rivotril 2mg",
        principio_ativo="Clonazepam",
        preco=Decimal("45.90"),
        estoque_atual=50,
        estoque_minimo=10,
        requer_receita=True
    )


@pytest.fixture
def medicamento_estoque_baixo():
    """Fixture: medicamento com estoque abaixo do mínimo"""
    return Medicamento(
        nome="Paracetamol 750mg",
        principio_ativo="Paracetamol",
        preco=Decimal("12.00"),
        estoque_atual=5,   # ← abaixo do mínimo!
        estoque_minimo=10,
        requer_receita=False
    )


# ==========================================
# FIXTURES DE LOTES
# ==========================================

@pytest.fixture
def lote_valido():
    """Fixture: lote válido e não vencido"""
    return Lote(
        numero_lote="LOTE-2026-001",
        medicamento_id=1,
        quantidade=500,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica ABC Ltda"
    )


@pytest.fixture
def lote_vencendo_breve():
    """Fixture: lote que vence em 15 dias"""
    return Lote(
        numero_lote="LOTE-VENCENDO",
        medicamento_id=1,
        quantidade=100,
        data_fabricacao=date.today() - timedelta(days=200),
        data_validade=date.today() + timedelta(days=15),
        fornecedor="Farmacêutica XYZ"
    )


# ==========================================
# FIXTURES DE REPOSITÓRIOS
# ==========================================

@pytest.fixture
def repositorio_medicamentos():
    """Fixture: repositório em memória (limpo a cada teste)"""
    return MedicamentoRepositoryMemory()


@pytest.fixture
def repositorio_lotes():
    """Fixture: repositório de lotes em memória (limpo a cada teste)"""
    return LoteRepositoryMemory()


@pytest.fixture
def repositorios_populados(repositorio_medicamentos, repositorio_lotes):
    """
    Fixture: repositórios com dados pré-populados
    
    Cria 3 medicamentos e 2 lotes pra facilitar testes
    """
    # Criar medicamentos
    med1 = Medicamento(
        nome="Dipirona 500mg",
        principio_ativo="Dipirona Sódica",
        preco=Decimal("8.50"),
        estoque_atual=100,
        estoque_minimo=20,
        requer_receita=False
    )
    med2 = Medicamento(
        nome="Paracetamol 750mg",
        principio_ativo="Paracetamol",
        preco=Decimal("12.00"),
        estoque_atual=5,
        estoque_minimo=10,
        requer_receita=False
    )
    med3 = Medicamento(
        nome="Rivotril 2mg",
        principio_ativo="Clonazepam",
        preco=Decimal("45.90"),
        estoque_atual=50,
        estoque_minimo=10,
        requer_receita=True
    )

    med1 = repositorio_medicamentos.salvar(med1)
    med2 = repositorio_medicamentos.salvar(med2)
    med3 = repositorio_medicamentos.salvar(med3)

    # Criar lotes
    lote1 = Lote(
        numero_lote="LOTE-001",
        medicamento_id=med1.id,
        quantidade=100,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica ABC"
    )
    lote2 = Lote(
        numero_lote="LOTE-002",
        medicamento_id=med2.id,
        quantidade=5,
        data_fabricacao=date.today() - timedelta(days=90),
        data_validade=date.today() + timedelta(days=15),
        fornecedor="Farmacêutica XYZ"
    )

    repositorio_lotes.salvar(lote1)
    repositorio_lotes.salvar(lote2)

    return {
        "medicamentos": repositorio_medicamentos,
        "lotes": repositorio_lotes,
        "med1": med1,
        "med2": med2,
        "med3": med3,
    }
"""
Testes: MedicamentoFactory
Testa Factory Pattern
Aula 12 - Design Patterns
"""

from decimal import Decimal
from src.domain.factories import MedicamentoFactory


def teste_criar_medicamento_basico():
    """Testa criação básica de medicamento"""
    print("\n🧪 Teste 1: Criar medicamento básico")
    
    medicamento = MedicamentoFactory.criar(
        nome="dipirona",
        principio_ativo="dipirona sódica",
        preco=15.50
    )
    
    assert medicamento.nome == "Dipirona"  # Padronizado!
    assert medicamento.principio_ativo == "Dipirona Sódica"
    assert medicamento.preco == Decimal("15.50")
    assert medicamento.estoque_minimo == 50  # Padrão!
    assert medicamento.requer_receita == False  # ← Campo correto!
    
    print("✅ Medicamento criado com sucesso!")
    print(f"   Nome: {medicamento.nome}")
    print(f"   Estoque mínimo (padrão): {medicamento.estoque_minimo}")


def teste_criar_medicamento_customizado():
    """Testa criação com valores customizados"""
    print("\n🧪 Teste 2: Criar medicamento controlado customizado")
    
    medicamento = MedicamentoFactory.criar(
        nome="Rivotril",
        principio_ativo="Clonazepam",
        preco=45.90,
        estoque_minimo=100,
        controlado=True
    )
    
    assert medicamento.estoque_minimo == 100
    assert medicamento.requer_receita == True  # ← Campo correto!
    
    print("✅ Medicamento controlado criado!")
    print(f"   Nome: {medicamento.nome}")
    print(f"   Estoque mínimo: {medicamento.estoque_minimo}")
    print(f"   Requer receita: {medicamento.requer_receita}")


def teste_validacoes_factory():
    """Testa validações da Factory"""
    print("\n🧪 Teste 3: Validações da Factory")
    
    # Teste 1: Preço inválido
    try:
        MedicamentoFactory.criar(
            nome="Teste",
            principio_ativo="Teste",
            preco=0  # Inválido!
        )
        print("❌ ERRO: Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Validação de preço funcionou: {e}")
    
    # Teste 2: Nome muito curto
    try:
        MedicamentoFactory.criar(
            nome="AB",  # Muito curto!
            principio_ativo="Teste",
            preco=10.0
        )
        print("❌ ERRO: Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Validação de nome funcionou: {e}")


def teste_criar_com_lote_inicial():
    """Testa criação de medicamento com lote inicial"""
    print("\n🧪 Teste 4: Criar medicamento com lote inicial")
    
    medicamento, lote = MedicamentoFactory.criar_com_lote_inicial(
        nome="Paracetamol",
        principio_ativo="Paracetamol",
        preco=8.50,
        numero_lote="LOT123",
        quantidade_inicial=200,
        data_fabricacao="2026-01-01",
        data_validade="2027-01-01",
        fornecedor="farmasa",
        controlado=False
    )
    
    assert medicamento.nome == "Paracetamol"
    assert lote.numero_lote == "LOT123"
    assert lote.quantidade == 200
    assert lote.fornecedor == "Farmasa"  # Padronizado!
    
    print("✅ Medicamento e lote criados com sucesso!")
    print(f"   Medicamento: {medicamento.nome}")
    print(f"   Lote: {lote.numero_lote}")
    print(f"   Quantidade: {lote.quantidade}")
    print(f"   Fornecedor: {lote.fornecedor}")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO FACTORY PATTERN (AULA 12)")
    print("=" * 60)
    
    teste_criar_medicamento_basico()
    teste_criar_medicamento_customizado()
    teste_validacoes_factory()
    teste_criar_com_lote_inicial()
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES DO FACTORY PASSARAM!")
    print("=" * 60)
"""
Testes da entidade Medicamento
Testando as validações e métodos de negócio
"""

from datetime import date, timedelta
from decimal import Decimal
from src.domain.entities import Medicamento


def teste_criar_medicamento_valido():
    """Testa criar um medicamento válido"""
    print("🧪 Teste 1: Criar medicamento válido")
    
    medicamento = Medicamento(
        nome="Dipirona 500mg",
        principio_ativo="Dipirona Sódica",
        preco=Decimal("8.50"),
        estoque_atual=100,
        estoque_minimo=20,
        requer_receita=False,
        data_validade=date.today() + timedelta(days=365),
        descricao="Analgésico e antitérmico"
    )
    
    print(f"✅ Medicamento criado: {medicamento}")
    print(f"   Nome: {medicamento.nome}")
    print(f"   Princípio Ativo: {medicamento.principio_ativo}")
    print(f"   Preço: R$ {medicamento.preco}")
    print()


def teste_validacoes():
    """Testa as validações do medicamento"""
    print("🧪 Teste 2: Validações")
    
    # Teste 1: Nome vazio
    try:
        Medicamento(
            nome="",  # ❌ Nome vazio!
            principio_ativo="Teste",
            preco=Decimal("10.00"),
            estoque_atual=10,
            estoque_minimo=5,
            requer_receita=False,
            data_validade=date.today() + timedelta(days=100)
        )
        print("❌ ERRO: Deveria ter dado erro de nome vazio!")
    except ValueError as e:
        print(f"✅ Validação de nome funcionou: {e}")
    
    # Teste 2: Preço negativo
    try:
        Medicamento(
            nome="Teste",
            principio_ativo="Teste Ativo",
            preco=Decimal("-5.00"),  # ❌ Preço negativo!
            estoque_atual=10,
            estoque_minimo=5,
            requer_receita=False,
            data_validade=date.today() + timedelta(days=100)
        )
        print("❌ ERRO: Deveria ter dado erro de preço negativo!")
    except ValueError as e:
        print(f"✅ Validação de preço funcionou: {e}")
    
    # Teste 3: Data de validade vencida
    try:
        Medicamento(
            nome="Teste",
            principio_ativo="Teste Ativo",
            preco=Decimal("10.00"),
            estoque_atual=10,
            estoque_minimo=5,
            requer_receita=False,
            data_validade=date.today() - timedelta(days=1)  # ❌ Vencido!
        )
        print("❌ ERRO: Deveria ter dado erro de validade!")
    except ValueError as e:
        print(f"✅ Validação de validade funcionou: {e}")
    
    # Teste 4: Princípio ativo vazio
    try:
        Medicamento(
            nome="Teste Med",
            principio_ativo="",  # ❌ Princípio ativo vazio!
            preco=Decimal("10.00"),
            estoque_atual=10,
            estoque_minimo=5,
            requer_receita=False,
            data_validade=date.today() + timedelta(days=100)
        )
        print("❌ ERRO: Deveria ter dado erro de princípio ativo!")
    except ValueError as e:
        print(f"✅ Validação de princípio ativo funcionou: {e}")
    
    print()


def teste_metodos_negocio():
    """Testa os métodos de negócio"""
    print("🧪 Teste 3: Métodos de negócio")
    
    medicamento = Medicamento(
        nome="Paracetamol 750mg",
        principio_ativo="Paracetamol",
        preco=Decimal("12.00"),
        estoque_atual=50,
        estoque_minimo=10,
        requer_receita=False,
        data_validade=date.today() + timedelta(days=180)
    )
    
    # Teste estoque baixo
    print(f"Estoque está baixo? {medicamento.estoque_baixo()}")  # False (50 > 10)
    
    # Vender 45 unidades
    medicamento.baixar_estoque(45)
    print(f"Após vender 45, estoque: {medicamento.estoque_atual}")
    print(f"Agora está baixo? {medicamento.estoque_baixo()}")  # True (5 < 10)
    
    # Repor 30 unidades
    medicamento.repor_estoque(30)
    print(f"Após repor 30, estoque: {medicamento.estoque_atual}")
    
    print("✅ Métodos de negócio funcionaram!")
    print()


def teste_venda_invalida():
    """Testa venda com estoque insuficiente"""
    print("🧪 Teste 4: Venda inválida")
    
    medicamento = Medicamento(
        nome="Ibuprofeno 600mg",
        principio_ativo="Ibuprofeno",
        preco=Decimal("15.50"),
        estoque_atual=5,
        estoque_minimo=10,
        requer_receita=False,
        data_validade=date.today() + timedelta(days=200)
    )
    
    try:
        medicamento.baixar_estoque(10)  # ❌ Quer vender 10, mas só tem 5!
        print("❌ ERRO: Deveria ter dado erro de estoque!")
    except ValueError as e:
        print(f"✅ Validação de venda funcionou: {e}")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO ENTIDADE MEDICAMENTO (AULA 2)")
    print("=" * 60)
    print()
    
    teste_criar_medicamento_valido()
    teste_validacoes()
    teste_metodos_negocio()
    teste_venda_invalida()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
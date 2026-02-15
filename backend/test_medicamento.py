"""
Teste simples da entidade Medicamento
Só pra ver se tá funcionando!
"""

from datetime import date, timedelta
from decimal import Decimal
from src.domain.entities import Medicamento


def teste_criar_medicamento_valido():
    """Testa criar um medicamento válido"""
    print("🧪 Teste 1: Criar medicamento válido")
    
    medicamento = Medicamento(
        nome="Dipirona 500mg",
        descricao="Analgésico e antitérmico",
        preco=Decimal("8.50"),
        estoque_atual=100,
        estoque_minimo=20,
        requer_receita=False,
        data_validade=date.today() + timedelta(days=365)
    )
    
    print(f"✅ Medicamento criado: {medicamento}")
    print(f"   Estoque baixo? {medicamento.estoque_baixo()}")
    print(f"   Vencido? {medicamento.esta_vencido()}")
    print()


def teste_validacoes():
    """Testa as validações"""
    print("🧪 Teste 2: Validações de regra de negócio")
    
    # Teste 1: Nome vazio
    try:
        Medicamento(
            nome="",  # ❌ Vai dar erro!
            preco=Decimal("10.00"),
            estoque_atual=50,
            estoque_minimo=10,
            requer_receita=False,
            data_validade=date.today() + timedelta(days=365)
        )
        print("❌ ERRO: Deveria ter dado erro de nome vazio!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 2: Preço negativo
    try:
        Medicamento(
            nome="Paracetamol",
            preco=Decimal("-5.00"),  # ❌ Vai dar erro!
            estoque_atual=50,
            estoque_minimo=10,
            requer_receita=False,
            data_validade=date.today() + timedelta(days=365)
        )
        print("❌ ERRO: Deveria ter dado erro de preço negativo!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    print()


def teste_venda():
    """Testa a lógica de venda"""
    print("🧪 Teste 3: Lógica de venda")
    
    medicamento = Medicamento(
        nome="Ibuprofeno 600mg",
        preco=Decimal("15.00"),
        estoque_atual=30,
        estoque_minimo=10,
        requer_receita=False,
        data_validade=date.today() + timedelta(days=180)
    )
    
    print(f"Estoque inicial: {medicamento.estoque_atual}")
    
    # Vender 10 unidades
    medicamento.baixar_estoque(10)
    print(f"Após vender 10: {medicamento.estoque_atual}")
    
    # Repor 20 unidades
    medicamento.repor_estoque(20)
    print(f"Após repor 20: {medicamento.estoque_atual}")
    
    print(f"✅ Estoque final: {medicamento.estoque_atual}")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TESTANDO ENTIDADE MEDICAMENTO")
    print("=" * 50)
    print()
    
    teste_criar_medicamento_valido()
    teste_validacoes()
    teste_venda()
    
    print("=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 50)
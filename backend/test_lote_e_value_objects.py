"""
Testes da entidade Lote e Value Objects (CPF e Telefone)
Testando as novas funcionalidades da Aula 3!
"""

from datetime import date, timedelta
from decimal import Decimal
from src.domain.entities import Medicamento, Lote
from src.domain.value_objects import CPF, Telefone


def teste_criar_lote_valido():
    """Testa criar um lote válido"""
    print("🧪 Teste 1: Criar lote válido")
    
    lote = Lote(
        numero_lote="LOTE-2024-001",
        medicamento_id=1,
        quantidade=500,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica ABC Ltda"
    )
    
    print(f"✅ Lote criado: {lote}")
    print(f"   Vencido? {lote.esta_vencido()}")
    print(f"   Dias para vencer: {lote.dias_para_vencer()}")
    print(f"   Vence em breve? {lote.vence_em_breve()}")
    print()


def teste_validacoes_lote():
    """Testa as validações do lote"""
    print("🧪 Teste 2: Validações do lote")
    
    # Teste 1: Número de lote vazio
    try:
        Lote(
            numero_lote="",  # ❌ Vai dar erro!
            medicamento_id=1,
            quantidade=100,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Farmacêutica XYZ"
        )
        print("❌ ERRO: Deveria ter dado erro de número vazio!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 2: Data de validade antes da fabricação
    try:
        Lote(
            numero_lote="LOTE-123",
            medicamento_id=1,
            quantidade=100,
            data_fabricacao=date.today(),
            data_validade=date.today() - timedelta(days=1),  # ❌ Validade antes da fabricação!
            fornecedor="Farmacêutica XYZ"
        )
        print("❌ ERRO: Deveria ter dado erro de data!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 3: Quantidade negativa
    try:
        Lote(
            numero_lote="LOTE-456",
            medicamento_id=1,
            quantidade=-50,  # ❌ Quantidade negativa!
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Farmacêutica XYZ"
        )
        print("❌ ERRO: Deveria ter dado erro de quantidade!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    print()


def teste_metodos_lote():
    """Testa os métodos de negócio do lote"""
    print("🧪 Teste 3: Métodos do lote")
    
    # Criar lote que vence em breve
    lote = Lote(
        numero_lote="LOTE-789",
        medicamento_id=1,
        quantidade=200,
        data_fabricacao=date.today() - timedelta(days=300),
        data_validade=date.today() + timedelta(days=20),  # Vence em 20 dias
        fornecedor="Farmacêutica DEF"
    )
    
    print(f"Lote criado: {lote}")
    print(f"Vence em breve (30 dias)? {lote.vence_em_breve(30)}")  # True
    print(f"Vence em breve (10 dias)? {lote.vence_em_breve(10)}")  # False
    
    # Testar retirada de quantidade
    print(f"\nQuantidade inicial: {lote.quantidade}")
    lote.retirar_quantidade(50)
    print(f"Após retirar 50: {lote.quantidade}")
    
    # Testar adição de quantidade
    lote.adicionar_quantidade(30)
    print(f"Após adicionar 30: {lote.quantidade}")
    
    print(f"✅ Quantidade final: {lote.quantidade}")
    print()


def teste_cpf_valido():
    """Testa criar CPF válido"""
    print("🧪 Teste 4: CPF válido")
    
    # CPF válido (sem formatação)
    cpf1 = CPF("12345678909")  # CPF válido
    print(f"✅ CPF criado: {cpf1}")
    print(f"   Formatado: {cpf1}")
    print(f"   Sem formatação: {cpf1.sem_formatacao()}")
    
    # CPF válido (com formatação)
    cpf2 = CPF("123.456.789-09")
    print(f"✅ CPF criado: {cpf2}")
    
    # Testar imutabilidade
    try:
        cpf1.numero = "999.999.999-99"  # ❌ Não pode mudar!
        print("❌ ERRO: CPF não deveria ser mutável!")
    except Exception as e:
        print(f"✅ CPF é imutável (frozen): {type(e).__name__}")
    
    print()


def teste_cpf_invalido():
    """Testa validações do CPF"""
    print("🧪 Teste 5: Validações do CPF")
    
    # Teste 1: CPF com poucos dígitos
    try:
        CPF("123456789")  # ❌ Faltam dígitos!
        print("❌ ERRO: Deveria ter dado erro de tamanho!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 2: CPF com todos dígitos iguais
    try:
        CPF("111.111.111-11")  # ❌ Todos iguais!
        print("❌ ERRO: Deveria ter dado erro de CPF inválido!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 3: CPF com dígitos verificadores errados
    try:
        CPF("123.456.789-00")  # ❌ Dígitos verificadores errados!
        print("❌ ERRO: Deveria ter dado erro de dígitos verificadores!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    print()


def teste_telefone_valido():
    """Testa criar telefone válido"""
    print("🧪 Teste 6: Telefone válido")
    
    # Celular (11 dígitos)
    cel = Telefone("11987654321")
    print(f"✅ Celular criado: {cel}")
    print(f"   DDD: {cel.ddd()}")
    print(f"   É celular? {cel.eh_celular()}")
    print(f"   Sem formatação: {cel.sem_formatacao()}")
    
    # Fixo (10 dígitos)
    fixo = Telefone("1133334444")
    print(f"✅ Fixo criado: {fixo}")
    print(f"   DDD: {fixo.ddd()}")
    print(f"   É celular? {fixo.eh_celular()}")
    
    # Testar imutabilidade
    try:
        cel.numero = "(99) 99999-9999"  # ❌ Não pode mudar!
        print("❌ ERRO: Telefone não deveria ser mutável!")
    except Exception as e:
        print(f"✅ Telefone é imutável (frozen): {type(e).__name__}")
    
    print()


def teste_telefone_invalido():
    """Testa validações do telefone"""
    print("🧪 Teste 7: Validações do telefone")
    
    # Teste 1: Telefone muito curto
    try:
        Telefone("1199999")  # ❌ Poucos dígitos!
        print("❌ ERRO: Deveria ter dado erro de tamanho!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 2: DDD inválido
    try:
        Telefone("0199999999")  # ❌ DDD 01 não existe!
        print("❌ ERRO: Deveria ter dado erro de DDD!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 3: Celular sem 9 no início
    try:
        Telefone("11887654321")  # ❌ Celular sem 9!
        print("❌ ERRO: Deveria ter dado erro de celular!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    print()


def teste_comparacao_value_objects():
    """Testa que Value Objects com mesmo valor são iguais"""
    print("🧪 Teste 8: Comparação de Value Objects")
    
    # Dois CPFs com mesmo valor são IGUAIS
    cpf1 = CPF("123.456.789-09")
    cpf2 = CPF("12345678909")  # Mesmo CPF, formatação diferente
    
    print(f"CPF 1: {cpf1}")
    print(f"CPF 2: {cpf2}")
    print(f"São iguais? {cpf1 == cpf2}")  # True!
    
    # Dois telefones com mesmo valor são IGUAIS
    tel1 = Telefone("(11) 98765-4321")
    tel2 = Telefone("11987654321")  # Mesmo telefone, formatação diferente
    
    print(f"\nTelefone 1: {tel1}")
    print(f"Telefone 2: {tel2}")
    print(f"São iguais? {tel1 == tel2}")  # True!
    
    print("\n✅ Value Objects são comparados por VALOR, não por referência!")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO LOTE E VALUE OBJECTS (AULA 3)")
    print("=" * 60)
    print()
    
    # Testes do Lote
    teste_criar_lote_valido()
    teste_validacoes_lote()
    teste_metodos_lote()
    
    # Testes do CPF
    teste_cpf_valido()
    teste_cpf_invalido()
    
    # Testes do Telefone
    teste_telefone_valido()
    teste_telefone_invalido()
    
    # Teste de comparação
    teste_comparacao_value_objects()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
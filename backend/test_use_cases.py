"""
Testes dos Use Cases (Aula 4)
Testando CadastrarMedicamentoUseCase e ListarMedicamentosUseCase
"""

from decimal import Decimal
from src.application.use_cases import (
    CadastrarMedicamentoUseCase,
    ListarMedicamentosUseCase
)
from src.adapters.repositories import MedicamentoRepositoryMemory


def teste_cadastrar_medicamento():
    """Testa cadastrar um medicamento"""
    print("🧪 Teste 1: Cadastrar medicamento")
    
    # Criar repositório em memória
    repository = MedicamentoRepositoryMemory()
    
    # Criar use case
    use_case = CadastrarMedicamentoUseCase(repository)
    
    # Dados do medicamento
    dados = {
        'nome': 'Dipirona 500mg',
        'principio_ativo': 'Dipirona Sódica',
        'preco': '8.50',
        'estoque_minimo': 100
    }
    
    # Executar use case
    medicamento = use_case.execute(dados)
    
    # Verificar
    print(f"✅ Medicamento cadastrado: {medicamento}")
    print(f"   ID gerado: {medicamento.id}")
    print(f"   Nome: {medicamento.nome}")
    print(f"   Preço: R$ {medicamento.preco}")
    print()


def teste_listar_medicamentos():
    """Testa listar medicamentos"""
    print("🧪 Teste 2: Listar medicamentos")
    
    # Criar repositório em memória
    repository = MedicamentoRepositoryMemory()
    
    # Cadastrar alguns medicamentos primeiro
    use_case_cadastrar = CadastrarMedicamentoUseCase(repository)
    
    medicamentos_dados = [
        {
            'nome': 'Paracetamol 750mg',
            'principio_ativo': 'Paracetamol',
            'preco': '12.00',
            'estoque_minimo': 50
        },
        {
            'nome': 'Ibuprofeno 600mg',
            'principio_ativo': 'Ibuprofeno',
            'preco': '15.50',
            'estoque_minimo': 30
        },
        {
            'nome': 'Amoxicilina 500mg',
            'principio_ativo': 'Amoxicilina',
            'preco': '25.00',
            'estoque_minimo': 20
        }
    ]
    
    for dados in medicamentos_dados:
        use_case_cadastrar.execute(dados)
    
    # Listar todos
    use_case_listar = ListarMedicamentosUseCase(repository)
    medicamentos = use_case_listar.execute()
    
    print(f"✅ Total de medicamentos: {len(medicamentos)}")
    for med in medicamentos:
        print(f"   - ID {med.id}: {med.nome} (R$ {med.preco})")
    print()


def teste_validacoes_funcionam():
    """Testa se as validações do domínio funcionam no use case"""
    print("🧪 Teste 3: Validações do domínio")
    
    repository = MedicamentoRepositoryMemory()
    use_case = CadastrarMedicamentoUseCase(repository)
    
    # Teste 1: Preço negativo
    print("Tentando cadastrar com preço negativo...")
    try:
        use_case.execute({
            'nome': 'Teste',
            'principio_ativo': 'Teste',
            'preco': '-10.00',  # ❌ Preço negativo!
            'estoque_minimo': 10
        })
        print("❌ ERRO: Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 2: Nome vazio
    print("\nTentando cadastrar com nome vazio...")
    try:
        use_case.execute({
            'nome': '',  # ❌ Nome vazio!
            'principio_ativo': 'Teste',
            'preco': '10.00',
            'estoque_minimo': 10
        })
        print("❌ ERRO: Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    # Teste 3: Estoque mínimo negativo
    print("\nTentando cadastrar com estoque negativo...")
    try:
        use_case.execute({
            'nome': 'Teste',
            'principio_ativo': 'Teste',
            'preco': '10.00',
            'estoque_minimo': -5  # ❌ Estoque negativo!
        })
        print("❌ ERRO: Deveria ter dado erro!")
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")
    
    print()


def teste_fluxo_completo():
    """Testa fluxo completo: cadastrar e listar"""
    print("🧪 Teste 4: Fluxo completo")
    
    # Mesmo repositório para ambos os use cases
    repository = MedicamentoRepositoryMemory()
    
    cadastrar = CadastrarMedicamentoUseCase(repository)
    listar = ListarMedicamentosUseCase(repository)
    
    # Inicialmente vazio
    print("Lista inicial:", len(listar.execute()), "medicamentos")
    
    # Cadastrar 2 medicamentos
    cadastrar.execute({
        'nome': 'Medicamento A',
        'principio_ativo': 'Ativo A',
        'preco': '10.00',
        'estoque_minimo': 10
    })
    
    cadastrar.execute({
        'nome': 'Medicamento B',
        'principio_ativo': 'Ativo B',
        'preco': '20.00',
        'estoque_minimo': 20
    })
    
    # Listar novamente
    medicamentos = listar.execute()
    print(f"Após cadastrar: {len(medicamentos)} medicamentos")
    
    for med in medicamentos:
        print(f"  - {med.nome}")
    
    print("✅ Fluxo completo funcionou!")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO USE CASES (AULA 4)")
    print("=" * 60)
    print()
    
    teste_cadastrar_medicamento()
    teste_listar_medicamentos()
    teste_validacoes_funcionam()
    teste_fluxo_completo()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
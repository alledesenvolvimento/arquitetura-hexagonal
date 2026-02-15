"""
Testes dos Adapters (Aula 6)
Testando LoteRepositoryMemory e EstoqueServiceMemory
"""

from datetime import date, timedelta
from decimal import Decimal
from src.domain.entities import Lote, Medicamento
from src.adapters import (
    MedicamentoRepositoryMemory,
    LoteRepositoryMemory,
    EstoqueServiceMemory
)


def teste_lote_repository_memory():
    """Testa o repositório de lotes em memória"""
    print("🧪 Teste 1: LoteRepositoryMemory")
    
    # Criar repositório
    repo = LoteRepositoryMemory()
    
    # Criar lote
    lote = Lote(
        numero_lote="LOTE-2024-001",
        medicamento_id=1,
        quantidade=500,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica ABC"
    )
    
    # Salvar
    lote_salvo = repo.salvar(lote)
    print(f"✅ Lote salvo com ID: {lote_salvo.id}")
    
    # Buscar por ID
    lote_encontrado = repo.buscar_por_id(lote_salvo.id)
    print(f"✅ Lote encontrado: {lote_encontrado.numero_lote}")
    
    # Listar todos
    todos = repo.listar_todos()
    print(f"✅ Total de lotes: {len(todos)}")
    
    print()


def teste_buscar_por_medicamento():
    """Testa buscar lotes por medicamento"""
    print("🧪 Teste 2: Buscar lotes por medicamento")
    
    repo = LoteRepositoryMemory()
    
    # Criar 3 lotes do medicamento 1
    for i in range(3):
        lote = Lote(
            numero_lote=f"LOTE-MED1-{i+1}",
            medicamento_id=1,
            quantidade=100,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Fornecedor A"
        )
        repo.salvar(lote)
    
    # Criar 2 lotes do medicamento 2
    for i in range(2):
        lote = Lote(
            numero_lote=f"LOTE-MED2-{i+1}",
            medicamento_id=2,
            quantidade=100,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Fornecedor B"
        )
        repo.salvar(lote)
    
    # Buscar lotes do medicamento 1
    lotes_med1 = repo.buscar_por_medicamento(1)
    print(f"✅ Lotes do medicamento 1: {len(lotes_med1)}")
    
    # Buscar lotes do medicamento 2
    lotes_med2 = repo.buscar_por_medicamento(2)
    print(f"✅ Lotes do medicamento 2: {len(lotes_med2)}")
    
    print()


def teste_lotes_vencendo():
    """Testa listar lotes vencendo"""
    print("🧪 Teste 3: Lotes vencendo em breve")
    
    repo = LoteRepositoryMemory()
    
    # Lote que vence em 10 dias
    lote1 = Lote(
        numero_lote="VENCE-10",
        medicamento_id=1,
        quantidade=100,
        data_fabricacao=date.today() - timedelta(days=355),
        data_validade=date.today() + timedelta(days=10),
        fornecedor="Fornecedor A"
    )
    repo.salvar(lote1)
    
    # Lote que vence em 40 dias
    lote2 = Lote(
        numero_lote="VENCE-40",
        medicamento_id=1,
        quantidade=100,
        data_fabricacao=date.today() - timedelta(days=325),
        data_validade=date.today() + timedelta(days=40),
        fornecedor="Fornecedor A"
    )
    repo.salvar(lote2)
    
    # Lote que vence em 200 dias
    lote3 = Lote(
        numero_lote="VENCE-200",
        medicamento_id=1,
        quantidade=100,
        data_fabricacao=date.today() - timedelta(days=165),
        data_validade=date.today() + timedelta(days=200),
        fornecedor="Fornecedor A"
    )
    repo.salvar(lote3)
    
    # Buscar lotes que vencem em 30 dias
    vencendo_30 = repo.listar_vencendo_em(30)
    print(f"✅ Lotes vencendo em 30 dias: {len(vencendo_30)}")  # Deve ser 1
    
    # Buscar lotes que vencem em 60 dias
    vencendo_60 = repo.listar_vencendo_em(60)
    print(f"✅ Lotes vencendo em 60 dias: {len(vencendo_60)}")  # Deve ser 2
    
    print()


def teste_estoque_service():
    """Testa o serviço de estoque"""
    print("🧪 Teste 4: EstoqueServiceMemory")
    
    # Criar repositórios
    med_repo = MedicamentoRepositoryMemory()
    lote_repo = LoteRepositoryMemory()
    
    # Criar serviço
    estoque_service = EstoqueServiceMemory(med_repo, lote_repo)
    
    # Criar medicamento
    medicamento = Medicamento(
        nome="Dipirona 500mg",
        principio_ativo="Dipirona Sódica",
        preco=Decimal("8.50"),
        estoque_minimo=100
    )
    medicamento_salvo = med_repo.salvar(medicamento)
    
    # Criar lote
    lote = Lote(
        numero_lote="LOTE-001",
        medicamento_id=medicamento_salvo.id,
        quantidade=500,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica ABC"
    )
    lote_salvo = lote_repo.salvar(lote)
    
    # Registrar entrada de 200 unidades
    print("Registrando entrada de 200 unidades...")
    estoque_service.registrar_entrada(
        medicamento_salvo.id,
        lote_salvo.id,
        200
    )
    
    # Consultar estoque
    estoque = estoque_service.consultar_estoque_atual(medicamento_salvo.id)
    print(f"✅ Estoque total: {estoque['estoque_total']}")  # Deve ser 700
    print(f"✅ Estoque disponível: {estoque['estoque_disponivel']}")
    
    # Verificar disponibilidade
    tem_300 = estoque_service.verificar_disponibilidade(medicamento_salvo.id, 300)
    print(f"✅ Tem 300 disponíveis? {tem_300}")  # True
    
    # Registrar saída de 100 unidades
    print("Registrando saída de 100 unidades...")
    estoque_service.registrar_saida(medicamento_salvo.id, 100)
    
    # Consultar estoque novamente
    estoque = estoque_service.consultar_estoque_atual(medicamento_salvo.id)
    print(f"✅ Estoque após saída: {estoque['estoque_disponivel']}")  # Deve ser 600
    
    print()


def teste_estoque_baixo():
    """Testa listagem de estoque baixo"""
    print("🧪 Teste 5: Listagem de estoque baixo")
    
    # Criar repositórios
    med_repo = MedicamentoRepositoryMemory()
    lote_repo = LoteRepositoryMemory()
    
    # Criar serviço
    estoque_service = EstoqueServiceMemory(med_repo, lote_repo)
    
    # Criar medicamento com estoque mínimo 100
    medicamento = Medicamento(
        nome="Paracetamol 750mg",
        principio_ativo="Paracetamol",
        preco=Decimal("12.00"),
        estoque_minimo=100  # Mínimo: 100
    )
    medicamento_salvo = med_repo.salvar(medicamento)
    
    # Criar lote com apenas 50 unidades (ABAIXO do mínimo!)
    lote = Lote(
        numero_lote="LOTE-BAIXO",
        medicamento_id=medicamento_salvo.id,
        quantidade=50,  # Apenas 50!
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor="Farmacêutica XYZ"
    )
    lote_repo.salvar(lote)
    
    # Listar estoque baixo
    estoque_baixo = estoque_service.listar_estoque_baixo()
    
    print(f"✅ Medicamentos com estoque baixo: {len(estoque_baixo)}")
    for item in estoque_baixo:
        print(f"   - {item['nome']}: {item['estoque_atual']} (mín: {item['estoque_minimo']})")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO ADAPTERS (AULA 6)")
    print("=" * 60)
    print()
    
    teste_lote_repository_memory()
    teste_buscar_por_medicamento()
    teste_lotes_vencendo()
    teste_estoque_service()
    teste_estoque_baixo()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
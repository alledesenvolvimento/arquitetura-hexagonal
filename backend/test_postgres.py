"""
Testes com PostgreSQL (Aula 7)
Testando LoteRepositoryPostgres
"""

from datetime import date, timedelta
from decimal import Decimal
from src.domain.entities import Lote, Medicamento
from src.adapters.repositories import LoteRepositoryPostgres
from src.infrastructure.database import SessionLocal, MedicamentoModel


def teste_salvar_lote_postgres():
    """Testa salvar lote no PostgreSQL"""
    print("🧪 Teste 1: Salvar lote no PostgreSQL")
    
    # Criar sessão
    session = SessionLocal()
    
    try:
        # PRIMEIRO: Criar medicamento no banco (pra ter a FK!)
        medicamento_model = MedicamentoModel(
            nome="Dipirona 500mg",
            principio_ativo="Dipirona Sódica",
            preco="8.50",
            estoque_minimo=100,
            estoque_atual=0,
            requer_receita=0
        )
        session.add(medicamento_model)
        session.commit()
        session.refresh(medicamento_model)
        
        print(f"📦 Medicamento criado com ID: {medicamento_model.id}")
        
        # AGORA SIM: Criar repositório PostgreSQL
        repo = LoteRepositoryPostgres(session)
        
        # Criar lote (usando o ID do medicamento criado)
        lote = Lote(
            numero_lote="POSTGRES-001",
            medicamento_id=medicamento_model.id,  # ← USA O ID REAL!
            quantidade=1000,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Farmacêutica PostgreSQL Ltda"
        )
        
        # Salvar
        lote_salvo = repo.salvar(lote)
        print(f"✅ Lote salvo no PostgreSQL com ID: {lote_salvo.id}")
        print(f"   Número: {lote_salvo.numero_lote}")
        print(f"   Quantidade: {lote_salvo.quantidade}")
        print(f"   Medicamento ID: {lote_salvo.medicamento_id}")
        
        # Buscar por ID
        lote_encontrado = repo.buscar_por_id(lote_salvo.id)
        print(f"✅ Lote buscado do PostgreSQL: {lote_encontrado.numero_lote}")
        
    finally:
        session.close()
    
    print()


def teste_listar_todos_postgres():
    """Testa listar todos os lotes do PostgreSQL"""
    print("🧪 Teste 2: Listar todos do PostgreSQL")
    
    session = SessionLocal()
    
    try:
        repo = LoteRepositoryPostgres(session)
        
        # Listar todos (inclui o lote do teste anterior)
        todos = repo.listar_todos()
        print(f"✅ Total de lotes no PostgreSQL: {len(todos)}")
        
        for lote in todos:
            print(f"   - ID {lote.id}: {lote.numero_lote} ({lote.quantidade} unidades)")
        
    finally:
        session.close()
    
    print()


def teste_buscar_por_medicamento_postgres():
    """Testa buscar lotes por medicamento no PostgreSQL"""
    print("🧪 Teste 3: Buscar por medicamento no PostgreSQL")
    
    session = SessionLocal()
    
    try:
        # Criar medicamento
        medicamento_model = MedicamentoModel(
            nome="Paracetamol 750mg",
            principio_ativo="Paracetamol",
            preco="12.00",
            estoque_minimo=50,
            estoque_atual=0,
            requer_receita=0
        )
        session.add(medicamento_model)
        session.commit()
        session.refresh(medicamento_model)
        
        print(f"📦 Medicamento criado com ID: {medicamento_model.id}")
        
        repo = LoteRepositoryPostgres(session)
        
        # Criar lotes do medicamento criado
        for i in range(3):
            lote = Lote(
                numero_lote=f"MED{medicamento_model.id}-LOTE-{i+1}",
                medicamento_id=medicamento_model.id,
                quantidade=500 + (i * 100),
                data_fabricacao=date.today() - timedelta(days=30),
                data_validade=date.today() + timedelta(days=365),
                fornecedor="Fornecedor Teste"
            )
            repo.salvar(lote)
        
        # Buscar lotes do medicamento
        lotes_med = repo.buscar_por_medicamento(medicamento_model.id)
        print(f"✅ Lotes do medicamento {medicamento_model.id}: {len(lotes_med)}")
        
        for lote in lotes_med:
            print(f"   - {lote.numero_lote}: {lote.quantidade} unidades")
        
    finally:
        session.close()
    
    print()


def teste_comparacao_memory_vs_postgres():
    """Compara Memory vs Postgres - MESMA INTERFACE!"""
    print("🧪 Teste 4: Comparação Memory vs Postgres")
    print("=" * 60)
    
    from src.adapters.repositories import LoteRepositoryMemory
    
    # TESTE 1: Memory
    print("\n📍 Usando Memory Adapter:")
    repo_memory = LoteRepositoryMemory()
    
    lote_memory = Lote(
        numero_lote='COMPARE-MEMORY',
        medicamento_id=999,  # Qualquer ID (não valida FK na memória)
        quantidade=750,
        data_fabricacao=date.today() - timedelta(days=30),
        data_validade=date.today() + timedelta(days=365),
        fornecedor='Fornecedor Memory'
    )
    
    lote_salvo_memory = repo_memory.salvar(lote_memory)
    print(f"   ✅ Salvo na memória com ID: {lote_salvo_memory.id}")
    
    # TESTE 2: PostgreSQL
    print("\n📍 Usando Postgres Adapter:")
    session = SessionLocal()
    try:
        # Criar medicamento pra ter FK válida
        medicamento_model = MedicamentoModel(
            nome="Ibuprofeno 600mg",
            principio_ativo="Ibuprofeno",
            preco="15.50",
            estoque_minimo=30,
            estoque_atual=0,
            requer_receita=0
        )
        session.add(medicamento_model)
        session.commit()
        session.refresh(medicamento_model)
        
        repo_postgres = LoteRepositoryPostgres(session)
        
        lote_postgres = Lote(
            numero_lote='COMPARE-POSTGRES',
            medicamento_id=medicamento_model.id,
            quantidade=750,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor='Fornecedor Postgres'
        )
        
        lote_salvo_postgres = repo_postgres.salvar(lote_postgres)
        print(f"   ✅ Salvo no PostgreSQL com ID: {lote_salvo_postgres.id}")
    finally:
        session.close()
    
    print("\n" + "=" * 60)
    print("🎉 MESMA INTERFACE, DIFERENTES IMPLEMENTAÇÕES!")
    print("   ↳ Trocamos o adapter SEM mexer no código!")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO POSTGRESQL (AULA 7)")
    print("=" * 60)
    print()
    
    teste_salvar_lote_postgres()
    teste_listar_todos_postgres()
    teste_buscar_por_medicamento_postgres()
    teste_comparacao_memory_vs_postgres()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
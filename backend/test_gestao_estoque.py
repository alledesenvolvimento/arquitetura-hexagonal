"""
Testes de Gestão de Estoque
Testando use cases de adicionar, remover e verificar estoque
"""

from datetime import date, timedelta
from sqlalchemy import text

from src.domain.entities import Medicamento, Lote
from src.adapters.repositories import (
    MedicamentoRepositoryPostgres,
    LoteRepositoryPostgres
)
from src.application.use_cases import (
    AdicionarEstoqueUseCase,
    RemoverEstoqueUseCase,
    VerificarEstoqueBaixoUseCase
)
from src.infrastructure.database import SessionLocal


def limpar_banco():
    """Limpa dados de teste do banco"""
    session = SessionLocal()
    try:
        session.execute(text("DELETE FROM lotes"))
        session.execute(text("DELETE FROM medicamentos"))
        session.commit()
        print("🧹 Banco limpo!\n")
    finally:
        session.close()


def teste_adicionar_estoque():
    """Testa adicionar estoque"""
    print("🧪 Teste 1: Adicionar Estoque")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        # 1. Criar repositórios
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        
        # 2. Cadastrar medicamento
        from decimal import Decimal
        from src.application.use_cases import CadastrarMedicamentoUseCase
        
        cadastrar_use_case = CadastrarMedicamentoUseCase(medicamento_repo)
        medicamento_data = {
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": Decimal("8.50"),
            "estoque_minimo": 100
        }
        medicamento = cadastrar_use_case.execute(medicamento_data)
        print(f"✅ Medicamento cadastrado: {medicamento.nome} (ID: {medicamento.id})")
        
        # 3. Adicionar estoque
        adicionar_use_case = AdicionarEstoqueUseCase(medicamento_repo, lote_repo)
        
        # Usar datas relativas (hoje + X dias) para garantir que sempre funcionem
        from datetime import date, timedelta
        hoje = date.today()
        data_fab = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")
        data_val = (hoje + timedelta(days=365)).strftime("%Y-%m-%d")
        
        resultado = adicionar_use_case.execute(
            medicamento_id=medicamento.id,
            quantidade=200,
            numero_lote="LOTE-2024-001",
            data_fabricacao=data_fab,
            data_validade=data_val,
            fornecedor="Farmacêutica ABC Ltda"
        )
        
        print(f"✅ Estoque adicionado!")
        print(f"   Quantidade: {resultado['lote_adicionado']['quantidade']}")
        print(f"   Lote: {resultado['lote_adicionado']['numero_lote']}")
        print(f"   Estoque Total: {resultado['estoque_atual']}")
        print(f"   Status: {resultado['status']}")
        print(f"   Mensagem: {resultado['mensagem']}")
        
    finally:
        session.close()
    
    print()


def teste_remover_estoque():
    """Testa remover estoque"""
    print("🧪 Teste 2: Remover Estoque")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        # 1. Criar repositórios
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        
        # 2. Buscar medicamento criado no teste anterior
        medicamentos = medicamento_repo.listar_todos()
        medicamento = medicamentos[0]
        print(f"📦 Medicamento: {medicamento.nome} (ID: {medicamento.id})")
        
        # Verificar estoque antes
        lotes = lote_repo.buscar_por_medicamento(medicamento.id)
        estoque_antes = sum(lote.quantidade for lote in lotes)
        print(f"📊 Estoque antes: {estoque_antes}")
        
        # 3. Remover estoque (venda)
        remover_use_case = RemoverEstoqueUseCase(medicamento_repo, lote_repo)
        
        resultado = remover_use_case.execute(
            medicamento_id=medicamento.id,
            quantidade=50,
            motivo="VENDA",
            observacao="Venda para cliente João Silva"
        )
        
        print(f"✅ Estoque removido!")
        print(f"   Quantidade removida: {resultado['quantidade_removida']}")
        print(f"   Motivo: {resultado['motivo']}")
        print(f"   Estoque Total: {resultado['estoque_atual']}")
        print(f"   Status: {resultado['status']}")
        print(f"   Mensagem: {resultado['mensagem']}")
        
    finally:
        session.close()
    
    print()


def teste_estoque_insuficiente():
    """Testa erro quando tenta remover mais do que tem"""
    print("🧪 Teste 3: Estoque Insuficiente")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        # 1. Criar repositórios
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        
        # 2. Buscar medicamento
        medicamentos = medicamento_repo.listar_todos()
        medicamento = medicamentos[0]
        
        # Verificar estoque atual
        lotes = lote_repo.buscar_por_medicamento(medicamento.id)
        estoque_atual = sum(lote.quantidade for lote in lotes if lote.data_validade > date.today())
        print(f"📊 Estoque atual: {estoque_atual}")
        
        # 3. Tentar remover mais do que tem
        remover_use_case = RemoverEstoqueUseCase(medicamento_repo, lote_repo)
        
        try:
            remover_use_case.execute(
                medicamento_id=medicamento.id,
                quantidade=999,  # Mais do que tem!
                motivo="VENDA"
            )
            print("❌ ERRO: Deveria ter dado erro de estoque insuficiente!")
        except ValueError as e:
            print(f"✅ Erro capturado corretamente: {str(e)}")
        
    finally:
        session.close()
    
    print()


def teste_verificar_estoque_baixo():
    """Testa verificação de estoque baixo"""
    print("🧪 Teste 4: Verificar Estoque Baixo")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        # 1. Criar repositórios
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        
        # 2. Criar medicamento com estoque baixo
        from decimal import Decimal
        from src.application.use_cases import CadastrarMedicamentoUseCase
        
        cadastrar_use_case = CadastrarMedicamentoUseCase(medicamento_repo)
        
        # Medicamento com estoque mínimo 100
        medicamento_critico = cadastrar_use_case.execute({
            "nome": "Paracetamol 750mg",
            "principio_ativo": "Paracetamol",
            "preco": Decimal("12.50"),
            "estoque_minimo": 100
        })
        
        # Adicionar apenas 30 unidades (abaixo do mínimo!)
        adicionar_use_case = AdicionarEstoqueUseCase(medicamento_repo, lote_repo)
        
        hoje = date.today()
        data_fab = (hoje - timedelta(days=30)).strftime("%Y-%m-%d")
        data_val = (hoje + timedelta(days=365)).strftime("%Y-%m-%d")
        
        adicionar_use_case.execute(
            medicamento_id=medicamento_critico.id,
            quantidade=30,
            numero_lote="LOTE-2024-002",
            data_fabricacao=data_fab,
            data_validade=data_val,
            fornecedor="Farmacêutica XYZ"
        )
        
        # 3. Verificar estoque baixo
        verificar_use_case = VerificarEstoqueBaixoUseCase(medicamento_repo, lote_repo)
        alertas = verificar_use_case.execute()
        
        print(f"⚠️ Medicamentos com estoque baixo: {len(alertas)}")
        print()
        
        for alerta in alertas:
            print(f"  📦 {alerta['nome']}")
            print(f"     Status: {alerta['status']}")
            print(f"     Estoque Atual: {alerta['estoque_atual']}")
            print(f"     Estoque Mínimo: {alerta['estoque_minimo']}")
            print(f"     Diferença: {alerta['diferenca']}")
            print()
        
    finally:
        session.close()
    
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TESTES DE GESTÃO DE ESTOQUE")
    print("=" * 50)
    print()
    
    # Limpar banco antes de começar
    limpar_banco()
    
    # Executar testes
    teste_adicionar_estoque()
    teste_remover_estoque()
    teste_estoque_insuficiente()
    teste_verificar_estoque_baixo()
    
    print("=" * 50)
    print("✅ Todos os testes concluídos!")
    print("=" * 50)
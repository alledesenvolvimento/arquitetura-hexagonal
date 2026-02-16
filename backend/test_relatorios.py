"""Testes dos Relatórios (Aula 11)"""

from decimal import Decimal
from datetime import date, timedelta

from src.infrastructure.database.base import SessionLocal, engine, Base
from src.adapters.repositories import MedicamentoRepositoryPostgres, LoteRepositoryPostgres
from src.application.use_cases import (
    CadastrarMedicamentoUseCase,
    RelatorioEstoqueUseCase,
    MedicamentosVencendoUseCase
)
from src.domain.entities import Lote


def limpar_banco():
    """Limpa e recria tabelas"""
    print("🗑️  Limpando banco...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Banco limpo!\n")


def criar_dados_teste():
    """Cria dados de teste"""
    print("📦 Criando dados...")
    session = SessionLocal()
    
    try:
        med_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        cadastrar = CadastrarMedicamentoUseCase(med_repo)
        
        # Medicamento OK
        med1 = cadastrar.execute({
            "nome": "Dipirona 500mg",
            "principio_ativo": "Dipirona Sódica",
            "preco": Decimal("8.50"),
            "estoque_minimo": 100,
            "requer_receita": False
        })
        
        lote1 = Lote(
            numero_lote="LOTE-DIP-001",
            medicamento_id=med1.id,
            quantidade=200,
            data_fabricacao=date.today() - timedelta(days=30),
            data_validade=date.today() + timedelta(days=365),
            fornecedor="Farmacêutica ABC"
        )
        lote_repo.salvar(lote1)
        
        # Medicamento BAIXO
        med2 = cadastrar.execute({
            "nome": "Paracetamol 750mg",
            "principio_ativo": "Paracetamol",
            "preco": Decimal("12.00"),
            "estoque_minimo": 100,
            "requer_receita": False
        })
        
        lote2 = Lote(
            numero_lote="LOTE-PAR-001",
            medicamento_id=med2.id,
            quantidade=50,
            data_fabricacao=date.today() - timedelta(days=20),
            data_validade=date.today() + timedelta(days=180),
            fornecedor="Farmacêutica XYZ"
        )
        lote_repo.salvar(lote2)
        
        # Medicamento VENCENDO
        med3 = cadastrar.execute({
            "nome": "Ibuprofeno 600mg",
            "principio_ativo": "Ibuprofeno",
            "preco": Decimal("15.00"),
            "estoque_minimo": 50,
            "requer_receita": False
        })
        
        lote3 = Lote(
            numero_lote="LOTE-IBU-001",
            medicamento_id=med3.id,
            quantidade=80,
            data_fabricacao=date.today() - timedelta(days=345),
            data_validade=date.today() + timedelta(days=10),
            fornecedor="Farmacêutica ABC"
        )
        lote_repo.salvar(lote3)
        
        session.commit()
        print("✅ Dados criados!\n")
        
    finally:
        session.close()


def teste_relatorio_estoque():
    """Testa relatório de estoque"""
    print("🧪 Teste 1: Relatório de Estoque")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        med_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        use_case = RelatorioEstoqueUseCase(med_repo, lote_repo)
        
        relatorio = use_case.execute(incluir_zerados=False)
        
        print(f"📊 RESUMO:")
        print(f"   Total produtos: {relatorio['resumo']['total_produtos']}")
        print(f"   Total unidades: {relatorio['resumo']['total_unidades']}")
        print(f"   Valor total: R$ {relatorio['resumo']['valor_total_estoque']:.2f}")
        
        print(f"\n🚨 ALERTAS:")
        for alerta in relatorio['alertas']:
            print(f"   [{alerta['tipo']}] {alerta['mensagem']}")
        
    finally:
        session.close()
    
    print()


def teste_medicamentos_vencendo():
    """Testa relatório de vencimentos"""
    print("🧪 Teste 2: Medicamentos Vencendo")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        med_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        use_case = MedicamentosVencendoUseCase(med_repo, lote_repo)
        
        relatorio = use_case.execute(dias=60)
        
        print(f"📊 RESUMO:")
        print(f"   Total produtos: {relatorio['resumo']['total_produtos']}")
        print(f"   Valor em risco: R$ {relatorio['resumo']['valor_total_risco']:.2f}")
        
        print(f"\n📦 PRODUTOS:")
        for produto in relatorio['produtos']:
            print(f"   - {produto['nome']}")
            print(f"     Vence em: {produto['dias_ate_primeiro_vencimento']} dias")
            print(f"     Urgência: {produto['urgencia']}")
        
    finally:
        session.close()
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO RELATÓRIOS (AULA 11)")
    print("=" * 60)
    print()
    
    limpar_banco()
    criar_dados_teste()
    teste_relatorio_estoque()
    teste_medicamentos_vencendo()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
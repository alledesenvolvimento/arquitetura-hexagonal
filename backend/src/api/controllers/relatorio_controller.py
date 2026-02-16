"""
Controller: Relatórios
Endpoints para consultas e relatórios gerenciais
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.database.base import SessionLocal
from src.adapters.repositories import MedicamentoRepositoryPostgres, LoteRepositoryPostgres
from src.application.use_cases import (
    RelatorioEstoqueUseCase,
    RelatorioMovimentacoesUseCase,
    MedicamentosVencendoUseCase
)
from src.api.schemas import (
    RelatorioEstoqueResponse,
    RelatorioMovimentacoesResponse,
    MedicamentosVencendoResponse
)


router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


def get_db():
    """Dependency para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/estoque",
    response_model=RelatorioEstoqueResponse,
    summary="Relatório de Estoque"
)
def relatorio_estoque(
    incluir_zerados: bool = Query(False, description="Incluir produtos zerados"),
    db: Session = Depends(get_db)
):
    """Gera relatório completo do estoque atual"""
    medicamento_repo = MedicamentoRepositoryPostgres(db)
    lote_repo = LoteRepositoryPostgres(db)
    use_case = RelatorioEstoqueUseCase(medicamento_repo, lote_repo)
    return use_case.execute(incluir_zerados=incluir_zerados)


@router.get(
    "/movimentacoes",
    response_model=RelatorioMovimentacoesResponse,
    summary="Relatório de Movimentações"
)
def relatorio_movimentacoes(
    dias: int = Query(30, ge=1, le=365, description="Período (dias)"),
    db: Session = Depends(get_db)
):
    """Gera relatório de entradas e saídas no período"""
    medicamento_repo = MedicamentoRepositoryPostgres(db)
    lote_repo = LoteRepositoryPostgres(db)
    use_case = RelatorioMovimentacoesUseCase(medicamento_repo, lote_repo)
    return use_case.execute(dias=dias)


@router.get(
    "/vencendo",
    response_model=MedicamentosVencendoResponse,
    summary="Medicamentos Vencendo"
)
def medicamentos_vencendo(
    dias: int = Query(60, ge=1, le=365, description="Dias para alertar"),
    db: Session = Depends(get_db)
):
    """Lista medicamentos que vencem nos próximos dias"""
    medicamento_repo = MedicamentoRepositoryPostgres(db)
    lote_repo = LoteRepositoryPostgres(db)
    use_case = MedicamentosVencendoUseCase(medicamento_repo, lote_repo)
    return use_case.execute(dias=dias)
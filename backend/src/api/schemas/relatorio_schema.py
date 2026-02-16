"""
Schemas: Relatórios
Estruturas de dados para relatórios e consultas
"""

from pydantic import BaseModel
from typing import List


# ============ RELATÓRIO DE ESTOQUE ============

class ItemEstoqueResponse(BaseModel):
    """Item individual do relatório de estoque"""
    medicamento_id: int
    nome: str
    principio_ativo: str
    preco_unitario: float
    estoque_atual: int
    estoque_minimo: int
    status: str
    prioridade: int
    valor_em_estoque: float
    total_lotes: int


class ResumoEstoqueResponse(BaseModel):
    """Resumo geral do estoque"""
    total_produtos: int
    total_unidades: int
    valor_total_estoque: float
    produtos_abaixo_minimo: int
    produtos_zerados: int
    produtos_ok: int


class AlertaEstoqueResponse(BaseModel):
    """Alerta do relatório de estoque"""
    tipo: str
    mensagem: str
    produtos: List[str]
    acao: str


class RelatorioEstoqueResponse(BaseModel):
    """Relatório completo de estoque"""
    resumo: ResumoEstoqueResponse
    itens: List[ItemEstoqueResponse]
    alertas: List[AlertaEstoqueResponse]


# ============ RELATÓRIO DE MOVIMENTAÇÕES ============

class LoteMovimentacaoResponse(BaseModel):
    """Lote dentro de uma movimentação"""
    numero_lote: str
    quantidade: int
    data_fabricacao: str
    data_validade: str


class MovimentacaoMedicamentoResponse(BaseModel):
    """Movimentação de um medicamento"""
    medicamento_id: int
    nome: str
    entradas: int
    saidas: int
    saldo: int
    lotes: List[LoteMovimentacaoResponse]


class PeriodoResponse(BaseModel):
    """Período do relatório"""
    data_inicial: str
    data_final: str
    dias: int


class ResumoMovimentacoesResponse(BaseModel):
    """Resumo das movimentações"""
    total_entradas: int
    total_saidas: int
    saldo: int
    total_medicamentos: int


class RelatorioMovimentacoesResponse(BaseModel):
    """Relatório de movimentações"""
    periodo: PeriodoResponse
    resumo: ResumoMovimentacoesResponse
    movimentacoes: List[MovimentacaoMedicamentoResponse]
    observacao: str


# ============ MEDICAMENTOS VENCENDO ============

class LoteVencendoResponse(BaseModel):
    """Lote vencendo"""
    numero_lote: str
    quantidade: int
    data_validade: str
    dias_restantes: int
    urgencia: str


class ProdutoVencendoResponse(BaseModel):
    """Produto vencendo"""
    medicamento_id: int
    nome: str
    principio_ativo: str
    preco_unitario: float
    lotes: List[LoteVencendoResponse]
    quantidade_total: int
    valor_total: float
    dias_ate_primeiro_vencimento: int
    urgencia: str
    prioridade: int
    acao_sugerida: str


class PeriodoAnaliseResponse(BaseModel):
    """Período de análise"""
    data_consulta: str
    dias_analisados: int
    data_limite: str


class UrgenciaResponse(BaseModel):
    """Contadores por urgência"""
    critica: int
    alta: int
    media: int


class ResumoVencimentosResponse(BaseModel):
    """Resumo de vencimentos"""
    total_produtos: int
    quantidade_total: int
    valor_total_risco: float
    por_urgencia: UrgenciaResponse


class AlertaVencimentoResponse(BaseModel):
    """Alerta de vencimento"""
    tipo: str
    mensagem: str
    acao: str


class MedicamentosVencendoResponse(BaseModel):
    """Relatório de medicamentos vencendo"""
    periodo_analise: PeriodoAnaliseResponse
    resumo: ResumoVencimentosResponse
    produtos: List[ProdutoVencendoResponse]
    alertas: List[AlertaVencimentoResponse]
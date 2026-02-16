"""
Schemas
Definições de estrutura de dados da API
"""

from .medicamento_schema import (
    MedicamentoCreate,
    MedicamentoResponse,
    MedicamentoUpdate
)
from .lote_schema import (
    LoteCreate,
    LoteResponse,
    LoteUpdate
)
from .estoque_schema import (
    AdicionarEstoqueRequest,
    RemoverEstoqueRequest,
    EstoqueResponse,
    EstoqueBaixoItem
)
from .receita_schema import (
    ReceitaValidarRequest,
    ReceitaValidarResponse
)

__all__ = [
    "MedicamentoCreate",
    "MedicamentoResponse",
    "MedicamentoUpdate",
    "LoteCreate",
    "LoteResponse",
    "LoteUpdate",
    "AdicionarEstoqueRequest",
    "RemoverEstoqueRequest",
    "EstoqueResponse",
    "EstoqueBaixoItem",
    "ReceitaValidarRequest",
    "ReceitaValidarResponse",
]
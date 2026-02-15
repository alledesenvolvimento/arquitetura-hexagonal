"""
Ports (Interfaces) do domínio AlleFarma
Definem os "contratos" que os adapters devem implementar
"""

from .medicamento_repository_port import MedicamentoRepositoryPort
from .lote_repository_port import LoteRepositoryPort
from .estoque_service_port import EstoqueServicePort

__all__ = [
    'MedicamentoRepositoryPort',
    'LoteRepositoryPort',
    'EstoqueServicePort'
]
"""
Repositories (Adapters de Persistência) do AlleFarma
Implementam os Ports definidos no domínio
"""

from .medicamento_repository_memory import MedicamentoRepositoryMemory
from .lote_repository_memory import LoteRepositoryMemory

__all__ = [
    'MedicamentoRepositoryMemory',
    'LoteRepositoryMemory'
]
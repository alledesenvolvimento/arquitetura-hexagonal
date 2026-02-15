"""
Adapters (Implementações) do AlleFarma
Conectam o domínio ao mundo externo
"""

from .repositories import (
    MedicamentoRepositoryMemory,
    LoteRepositoryMemory
)
from .services import EstoqueServiceMemory

__all__ = [
    'MedicamentoRepositoryMemory',
    'LoteRepositoryMemory',
    'EstoqueServiceMemory'
]
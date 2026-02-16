"""
Adapters (Implementações) do AlleFarma
Conectam o domínio ao mundo externo
"""

from .repositories import (
    MedicamentoRepositoryMemory,
    MedicamentoRepositoryPostgres,
    LoteRepositoryMemory,
    LoteRepositoryPostgres
)

__all__ = [
    "MedicamentoRepositoryMemory",
    "MedicamentoRepositoryPostgres",
    "LoteRepositoryMemory",
    "LoteRepositoryPostgres",
]
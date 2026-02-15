"""
Repositories (Adapters de Persistência) do AlleFarma
Implementam os Ports definidos no domínio
"""

from .medicamento_repository_memory import MedicamentoRepositoryMemory

__all__ = ['MedicamentoRepositoryMemory']
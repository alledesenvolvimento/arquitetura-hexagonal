"""
Ports (Interfaces) do domínio AlleFarma
Definem os "contratos" que os adapters devem implementar
"""

from .medicamento_repository_port import MedicamentoRepositoryPort

__all__ = ['MedicamentoRepositoryPort']
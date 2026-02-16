"""
Adapters Observers
Observers concretos que reagem a eventos
"""

from .base_observer import BaseObserver
from .estoque_baixo_observer import EstoqueBaixoObserver
from .produto_vencendo_observer import ProdutoVencendoObserver

__all__ = [
    "BaseObserver",
    "EstoqueBaixoObserver",
    "ProdutoVencendoObserver",
]
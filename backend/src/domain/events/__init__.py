"""
Domain Events
Eventos que acontecem no domínio
"""

from .base_event import BaseEvent
from .estoque_events import (
    EstoqueBaixoEvent,
    ProdutoVencendoEvent,
    EstoqueAtualizadoEvent
)

__all__ = [
    "BaseEvent",
    "EstoqueBaixoEvent",
    "ProdutoVencendoEvent",
    "EstoqueAtualizadoEvent",
]
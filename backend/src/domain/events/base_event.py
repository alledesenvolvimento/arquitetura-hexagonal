"""
Base para eventos do sistema
Observer Pattern - parte dos Events
"""

from abc import ABC
from datetime import datetime
from typing import Any, Dict


class BaseEvent(ABC):
    """
    Classe base para todos os eventos do sistema
    
    Evento = algo que aconteceu no sistema
    Exemplo: EstoqueBaixoEvent, ProdutoVencendoEvent
    """
    
    def __init__(self):
        """Inicializa evento com timestamp"""
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte evento pra dicionário
        Útil pra serializar e enviar
        """
        return {
            "tipo": self.__class__.__name__,
            "timestamp": self.timestamp.isoformat(),
            "dados": self._dados_especificos()
        }
    
    def _dados_especificos(self) -> Dict[str, Any]:
        """
        Sobrescrever em classes filhas
        Retorna dados específicos do evento
        """
        return {}
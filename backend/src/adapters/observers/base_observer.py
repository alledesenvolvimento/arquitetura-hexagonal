"""
Base Observer
Interface para todos os observers
"""

from abc import ABC, abstractmethod
from src.domain.events import BaseEvent


class BaseObserver(ABC):
    """
    Interface base para observers
    
    Observer = quem "ouve" eventos e reage
    """
    
    @abstractmethod
    def notificar(self, evento: BaseEvent):
        """
        Método chamado quando evento acontece
        
        Args:
            evento: Evento que foi disparado
        """
        pass
"""
Services (Adapters de Serviços) do AlleFarma
Implementam os Service Ports definidos no domínio
"""

from .estoque_service_memory import EstoqueServiceMemory

__all__ = ['EstoqueServiceMemory']
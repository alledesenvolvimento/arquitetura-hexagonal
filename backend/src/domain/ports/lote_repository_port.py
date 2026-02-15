
"""
Port (Interface) do Repositório de Lotes
Define o "contrato" para persistência de Lotes
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import date
from ..entities import Lote


class LoteRepositoryPort(ABC):
    """Interface para operações de persistência de Lotes"""
    
    @abstractmethod
    def salvar(self, lote: Lote) -> Lote:
        """
        Salva um lote e retorna com ID gerado
        
        Args:
            lote: Entidade Lote a ser salva
            
        Returns:
            Lote salvo (com ID preenchido)
        """
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Lote]:
        """
        Busca lote por ID
        
        Args:
            id: ID do lote
            
        Returns:
            Lote encontrado ou None se não existir
        """
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Lote]:
        """
        Lista todos os lotes
        
        Returns:
            Lista de lotes (pode ser vazia)
        """
        pass
    
    @abstractmethod
    def buscar_por_medicamento(self, medicamento_id: int) -> List[Lote]:
        """
        Busca todos os lotes de um medicamento específico
        
        Args:
            medicamento_id: ID do medicamento
            
        Returns:
            Lista de lotes do medicamento (pode ser vazia)
        """
        pass
    
    @abstractmethod
    def listar_vencendo_em(self, dias: int) -> List[Lote]:
        """
        Lista lotes que vencem nos próximos X dias
        
        Args:
            dias: Número de dias pra verificar
            
        Returns:
            Lista de lotes que vencem nos próximos X dias
        """
        pass
    
    @abstractmethod
    def atualizar(self, lote: Lote) -> Lote:
        """
        Atualiza um lote existente
        
        Args:
            lote: Lote com dados atualizados
            
        Returns:
            Lote atualizado
            
        Raises:
            ValueError: Se lote não existir
        """
        pass
    
    @abstractmethod
    def deletar(self, id: int) -> bool:
        """
        Deleta um lote pelo ID
        
        Args:
            id: ID do lote a deletar
            
        Returns:
            True se deletou, False se não encontrou
        """
        pass
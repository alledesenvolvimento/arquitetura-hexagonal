"""
Port (Interface) do Repositório de Medicamentos
Define o "contrato" que qualquer repositório de medicamentos deve seguir

Este é um PORT - uma interface abstrata que será implementada pelos Adapters
"""

from abc import ABC, abstractmethod
from typing import Optional
from ..entities import Medicamento


class MedicamentoRepositoryPort(ABC):
    """
    Interface que define as operações de persistência de Medicamentos
    
    Qualquer classe que implemente esta interface DEVE ter esses métodos.
    Isso permite trocar a implementação (memória, PostgreSQL, MongoDB...)
    sem afetar o resto do código!
    """
    
    @abstractmethod
    def salvar(self, medicamento: Medicamento) -> Medicamento:
        """
        Salva um medicamento e retorna o medicamento salvo (com ID gerado)
        
        Args:
            medicamento: Entidade Medicamento a ser salva
            
        Returns:
            Medicamento salvo (com ID preenchido)
        """
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Medicamento]:
        """
        Busca um medicamento pelo ID
        
        Args:
            id: ID do medicamento
            
        Returns:
            Medicamento encontrado ou None se não existir
        """
        pass
    
    @abstractmethod
    def listar_todos(self) -> list[Medicamento]:
        """
        Lista todos os medicamentos cadastrados
        
        Returns:
            Lista de medicamentos (pode ser vazia)
        """
        pass
    
    @abstractmethod
    def atualizar(self, medicamento: Medicamento) -> Medicamento:
        """
        Atualiza um medicamento existente
        
        Args:
            medicamento: Medicamento com dados atualizados
            
        Returns:
            Medicamento atualizado
            
        Raises:
            ValueError: Se medicamento não existir
        """
        pass
    
    @abstractmethod
    def deletar(self, id: int) -> bool:
        """
        Deleta um medicamento pelo ID
        
        Args:
            id: ID do medicamento a deletar
            
        Returns:
            True se deletou, False se não encontrou
        """
        pass
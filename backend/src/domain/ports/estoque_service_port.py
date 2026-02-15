"""
Port (Interface) do Serviço de Estoque
Define o "contrato" para operações de estoque
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class EstoqueServicePort(ABC):
    """Interface para serviço de controle de estoque"""
    
    @abstractmethod
    def verificar_disponibilidade(self, medicamento_id: int, quantidade: int) -> bool:
        """
        Verifica se tem quantidade disponível de um medicamento
        
        Args:
            medicamento_id: ID do medicamento
            quantidade: Quantidade desejada
            
        Returns:
            True se tem disponível, False caso contrário
        """
        pass
    
    @abstractmethod
    def registrar_entrada(self, medicamento_id: int, lote_id: int, quantidade: int) -> None:
        """
        Registra entrada de estoque (compra/recebimento)
        
        Args:
            medicamento_id: ID do medicamento
            lote_id: ID do lote recebido
            quantidade: Quantidade recebida
            
        Raises:
            ValueError: Se dados inválidos
        """
        pass
    
    @abstractmethod
    def registrar_saida(self, medicamento_id: int, quantidade: int) -> None:
        """
        Registra saída de estoque (venda)
        
        Args:
            medicamento_id: ID do medicamento
            quantidade: Quantidade vendida
            
        Raises:
            ValueError: Se estoque insuficiente ou dados inválidos
        """
        pass
    
    @abstractmethod
    def consultar_estoque_atual(self, medicamento_id: int) -> Dict[str, int]:
        """
        Retorna informações de estoque de um medicamento
        
        Args:
            medicamento_id: ID do medicamento
            
        Returns:
            Dicionário com informações de estoque:
            {
                "estoque_total": X,
                "estoque_disponivel": Y,
                "estoque_reservado": Z
            }
        """
        pass
    
    @abstractmethod
    def listar_estoque_baixo(self) -> List[Dict]:
        """
        Lista medicamentos com estoque abaixo do mínimo
        
        Returns:
            Lista de dicionários com informações dos medicamentos:
            [
                {
                    "medicamento_id": X,
                    "nome": "...",
                    "estoque_atual": Y,
                    "estoque_minimo": Z
                },
                ...
            ]
        """
        pass
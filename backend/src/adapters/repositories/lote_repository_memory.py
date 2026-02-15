"""
Adapter: Repositório de Lotes em Memória
Implementa o LoteRepositoryPort guardando dados na memória (RAM)

ATENÇÃO: Quando o programa encerra, os dados são perdidos!
Isso é apenas para testes. Nas próximas aulas faremos com banco real.
"""

from typing import Optional, List
from datetime import date, timedelta
from src.domain.entities import Lote
from src.domain.ports import LoteRepositoryPort


class LoteRepositoryMemory(LoteRepositoryPort):
    """
    Implementação em memória do repositório de lotes
    
    Armazena lotes em um dicionário Python (RAM)
    Quando o programa fecha, perde tudo!
    """
    
    def __init__(self):
        """Inicializa o repositório vazio"""
        self._lotes: dict[int, Lote] = {}
        self._proximo_id = 1
    
    def salvar(self, lote: Lote) -> Lote:
        """
        Salva lote na memória
        
        Args:
            lote: Lote a ser salvo
            
        Returns:
            Lote salvo (com ID gerado)
        """
        # Gera ID se não tiver
        if lote.id is None:
            lote.id = self._proximo_id
            self._proximo_id += 1
        
        # Salva no dicionário
        self._lotes[lote.id] = lote
        
        return lote
    
    def buscar_por_id(self, id: int) -> Optional[Lote]:
        """
        Busca lote por ID
        
        Args:
            id: ID do lote
            
        Returns:
            Lote encontrado ou None
        """
        return self._lotes.get(id)
    
    def listar_todos(self) -> List[Lote]:
        """
        Lista todos os lotes
        
        Returns:
            Lista de todos os lotes cadastrados
        """
        return list(self._lotes.values())
    
    def buscar_por_medicamento(self, medicamento_id: int) -> List[Lote]:
        """
        Busca todos os lotes de um medicamento específico
        
        Args:
            medicamento_id: ID do medicamento
            
        Returns:
            Lista de lotes do medicamento
        """
        return [
            lote for lote in self._lotes.values()
            if lote.medicamento_id == medicamento_id
        ]
    
    def listar_vencendo_em(self, dias: int) -> List[Lote]:
        """
        Lista lotes que vencem nos próximos X dias
        
        Args:
            dias: Número de dias para verificar
            
        Returns:
            Lista de lotes que vencem nos próximos X dias
        """
        data_limite = date.today() + timedelta(days=dias)
        
        return [
            lote for lote in self._lotes.values()
            if lote.data_validade <= data_limite
            and lote.data_validade >= date.today()  # Não incluir vencidos
        ]
    
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
        if lote.id is None:
            raise ValueError("Lote precisa ter ID para atualizar!")
        
        if lote.id not in self._lotes:
            raise ValueError(f"Lote {lote.id} não encontrado!")
        
        self._lotes[lote.id] = lote
        return lote
    
    def deletar(self, id: int) -> bool:
        """
        Deleta um lote pelo ID
        
        Args:
            id: ID do lote a deletar
            
        Returns:
            True se deletou, False se não encontrou
        """
        if id in self._lotes:
            del self._lotes[id]
            return True
        return False
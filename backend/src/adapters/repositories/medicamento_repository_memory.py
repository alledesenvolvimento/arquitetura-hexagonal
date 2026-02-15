"""
Adapter: Repositório de Medicamentos em Memória
Implementa o MedicamentoRepositoryPort guardando dados na memória (RAM)

ATENÇÃO: Quando o programa encerra, os dados são perdidos!
Isso é apenas para testes. Nas próximas aulas faremos com banco real.
"""

from typing import Optional
from src.domain.entities import Medicamento
from src.domain.ports import MedicamentoRepositoryPort


class MedicamentoRepositoryMemory(MedicamentoRepositoryPort):
    """
    Implementação em memória do repositório de medicamentos
    
    Armazena medicamentos em um dicionário Python (RAM)
    Quando o programa fecha, perde tudo!
    """
    
    def __init__(self):
        """Inicializa o repositório vazio"""
        self._medicamentos: dict[int, Medicamento] = {}
        self._proximo_id = 1
    
    def salvar(self, medicamento: Medicamento) -> Medicamento:
        """Salva medicamento na memória"""
        # Gera ID se não tiver
        if medicamento.id is None:
            medicamento.id = self._proximo_id
            self._proximo_id += 1
        
        # Salva no dicionário
        self._medicamentos[medicamento.id] = medicamento
        
        return medicamento
    
    def buscar_por_id(self, id: int) -> Optional[Medicamento]:
        """Busca medicamento por ID"""
        return self._medicamentos.get(id)
    
    def listar_todos(self) -> list[Medicamento]:
        """Lista todos os medicamentos"""
        return list(self._medicamentos.values())
    
    def atualizar(self, medicamento: Medicamento) -> Medicamento:
        """Atualiza medicamento existente"""
        if medicamento.id is None:
            raise ValueError("Medicamento precisa ter ID para atualizar!")
        
        if medicamento.id not in self._medicamentos:
            raise ValueError(f"Medicamento {medicamento.id} não encontrado!")
        
        self._medicamentos[medicamento.id] = medicamento
        return medicamento
    
    def deletar(self, id: int) -> bool:
        """Deleta medicamento por ID"""
        if id in self._medicamentos:
            del self._medicamentos[id]
            return True
        return False
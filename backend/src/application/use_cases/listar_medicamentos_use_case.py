"""
Use Case: Listar Medicamentos
Coordena o processo de listar todos os medicamentos cadastrados
"""

from src.domain.entities import Medicamento
from src.domain.ports import MedicamentoRepositoryPort


class ListarMedicamentosUseCase:
    """
    Caso de Uso para listar todos os medicamentos
    
    Responsabilidades:
    - Buscar todos os medicamentos usando o repositório
    - Retornar lista de medicamentos
    """
    
    def __init__(self, repository: MedicamentoRepositoryPort):
        """
        Inicializa o Use Case com suas dependências
        
        Args:
            repository: Port do repositório de medicamentos
        """
        self.repository = repository
    
    def execute(self) -> list[Medicamento]:
        """
        Executa o caso de uso de listar medicamentos
        
        Returns:
            Lista de medicamentos cadastrados (pode ser vazia)
        """
        # Busca todos os medicamentos
        return self.repository.listar_todos()
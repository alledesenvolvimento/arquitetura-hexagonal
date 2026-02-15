"""
Use Case: Cadastrar Medicamento
Coordena o processo de cadastrar um novo medicamento no sistema
"""

from decimal import Decimal
from src.domain.entities import Medicamento
from src.domain.ports import MedicamentoRepositoryPort


class CadastrarMedicamentoUseCase:
    """
    Caso de Uso para cadastrar um novo medicamento
    
    Responsabilidades:
    - Receber dados do medicamento
    - Criar entidade Medicamento (validações ocorrem aqui!)
    - Salvar usando o repositório (port)
    - Retornar medicamento salvo
    """
    
    def __init__(self, repository: MedicamentoRepositoryPort):
        """
        Inicializa o Use Case com suas dependências
        
        Args:
            repository: Port do repositório de medicamentos
        """
        self.repository = repository
    
    def execute(self, dados: dict) -> Medicamento:
        """
        Executa o caso de uso de cadastrar medicamento
        
        Args:
            dados: Dicionário com os dados do medicamento
                - nome (str): Nome do medicamento
                - principio_ativo (str): Princípio ativo
                - preco (str/float): Preço
                - estoque_minimo (int): Estoque mínimo
                
        Returns:
            Medicamento cadastrado (com ID gerado)
            
        Raises:
            ValueError: Se dados inválidos (regras do domínio)
        """
        # PASSO 1: Criar entidade do domínio
        # (Todas as validações acontecem automaticamente aqui!)
        medicamento = Medicamento(
            nome=dados['nome'],
            principio_ativo=dados['principio_ativo'],
            preco=Decimal(str(dados['preco'])),
            estoque_minimo=dados['estoque_minimo']
        )
        
        # PASSO 2: Salvar usando o port
        medicamento_salvo = self.repository.salvar(medicamento)
        
        # PASSO 3: Retornar resultado
        return medicamento_salvo
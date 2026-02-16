"""
Use Case: Cadastrar Medicamento
Coordena o processo de cadastrar um novo medicamento no sistema
Agora com Factory Pattern! 🏭
"""

from decimal import Decimal
from typing import Dict, Any, Optional

from src.domain.entities import Medicamento, Lote
from src.domain.ports import MedicamentoRepositoryPort, LoteRepositoryPort
from src.domain.factories import MedicamentoFactory


class CadastrarMedicamentoUseCase:
    """
    Caso de Uso para cadastrar um novo medicamento
    
    Responsabilidades:
    - Receber dados do medicamento
    - Criar entidade Medicamento usando Factory! 🏭
    - Salvar usando o repositório (port)
    - Retornar medicamento salvo
    """
    
    def __init__(
        self, 
        repository: MedicamentoRepositoryPort,
        lote_repository: Optional[LoteRepositoryPort] = None
    ):
        """
        Inicializa o Use Case com suas dependências
        
        Args:
            repository: Port do repositório de medicamentos
            lote_repository: Port do repositório de lotes (opcional)
        """
        self.repository = repository
        self.lote_repository = lote_repository
    
    def execute(self, dados: dict) -> Medicamento:
        """
        Executa o caso de uso de cadastrar medicamento
        
        Args:
            dados: Dicionário com os dados do medicamento
                - nome (str): Nome do medicamento
                - principio_ativo (str): Princípio ativo
                - preco (str/float/Decimal): Preço
                - estoque_minimo (int): Estoque mínimo
                - requer_receita (bool, opcional): Se é controlado (Aula 10)
                
        Returns:
            Medicamento cadastrado (com ID gerado)
            
        Raises:
            ValueError: Se dados inválidos (regras do domínio)
        """
        # Converter preço para float (Factory espera float)
        preco = dados['preco']
        if isinstance(preco, Decimal):
            preco = float(preco)
        elif isinstance(preco, str):
            preco = float(preco)
        
        # USAR FACTORY para criar medicamento! 🏭
        medicamento = MedicamentoFactory.criar(
            nome=dados['nome'],
            principio_ativo=dados['principio_ativo'],
            preco=preco,
            estoque_minimo=dados.get('estoque_minimo'),  # Usa padrão da Factory se None
            controlado=dados.get('requer_receita', False)  # Compatível com campo atual
        )
        
        # Salvar usando o port
        medicamento_salvo = self.repository.salvar(medicamento)
        
        # Retornar resultado
        return medicamento_salvo
    
    def execute_com_lote_inicial(
        self,
        # Dados do medicamento
        nome: str,
        principio_ativo: str,
        preco: float,
        requer_receita: bool,
        estoque_minimo: Optional[int],
        # Dados do lote
        numero_lote: str,
        quantidade_inicial: int,
        data_fabricacao: str,
        data_validade: str,
        fornecedor: str
    ) -> Dict[str, Any]:
        """
        Cadastra medicamento JÁ COM lote inicial
        
        Usa Factory.criar_com_lote_inicial()! 🏭
        
        Novo método adicionado na Aula 12!
        """
        if not self.lote_repository:
            raise ValueError("Repositório de lotes não configurado")
        
        # Criar medicamento + lote usando Factory! 🏭
        medicamento, lote = MedicamentoFactory.criar_com_lote_inicial(
            nome=nome,
            principio_ativo=principio_ativo,
            preco=preco,
            numero_lote=numero_lote,
            quantidade_inicial=quantidade_inicial,
            data_fabricacao=data_fabricacao,
            data_validade=data_validade,
            fornecedor=fornecedor,
            estoque_minimo=estoque_minimo,
            controlado=requer_receita  # Converte aqui para o padrão da Factory
        )
        
        # Salvar medicamento
        medicamento_salvo = self.repository.salvar(medicamento)
        
        # Atualizar ID do medicamento no lote
        lote.medicamento_id = medicamento_salvo.id
        
        # Salvar lote
        lote_salvo = self.lote_repository.salvar(lote)
        
        # Retornar dados completos
        return {
            "medicamento": {
                "id": medicamento_salvo.id,
                "nome": medicamento_salvo.nome,
                "principio_ativo": medicamento_salvo.principio_ativo,
                "preco": float(medicamento_salvo.preco),
                "requer_receita": medicamento_salvo.requer_receita  # ← Campo correto!
            },
            "lote": {
                "id": lote_salvo.id,
                "numero_lote": lote_salvo.numero_lote,
                "quantidade": lote_salvo.quantidade,
                "data_fabricacao": lote_salvo.data_fabricacao.isoformat(),
                "data_validade": lote_salvo.data_validade.isoformat(),
                "fornecedor": lote_salvo.fornecedor
            },
            "mensagem": "Medicamento e lote inicial cadastrados com sucesso!"
        }
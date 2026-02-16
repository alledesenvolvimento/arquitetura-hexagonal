"""
Use Case: Adicionar Estoque
Responsável por adicionar produtos ao estoque (entrada)
"""

from datetime import datetime
from typing import Dict, Any

from src.domain.entities import Lote
from src.domain.ports import (
    MedicamentoRepositoryPort,
    LoteRepositoryPort
)


class AdicionarEstoqueUseCase:
    """
    Use Case para adicionar estoque
    
    Fluxo:
    1. Valida se medicamento existe
    2. Cria novo lote com os produtos recebidos
    3. Salva lote no banco
    4. Retorna informações atualizadas do estoque
    
    Regras de Negócio:
    - Quantidade deve ser maior que zero
    - Medicamento deve existir no cadastro
    - Lote deve ter data de validade futura
    """
    
    def __init__(
        self,
        medicamento_repository: MedicamentoRepositoryPort,
        lote_repository: LoteRepositoryPort
    ):
        """
        Inicializa o use case
        
        Args:
            medicamento_repository: Repositório de medicamentos
            lote_repository: Repositório de lotes
        """
        self.medicamento_repo = medicamento_repository
        self.lote_repo = lote_repository
    
    def execute(
        self,
        medicamento_id: int,
        quantidade: int,
        numero_lote: str,
        data_fabricacao: str,
        data_validade: str,
        fornecedor: str
    ) -> Dict[str, Any]:
        """
        Executa o caso de uso
        
        Args:
            medicamento_id: ID do medicamento
            quantidade: Quantidade a adicionar
            numero_lote: Número do lote
            data_fabricacao: Data de fabricação (YYYY-MM-DD)
            data_validade: Data de validade (YYYY-MM-DD)
            fornecedor: Nome do fornecedor
            
        Returns:
            Dicionário com informações do estoque atualizado
            
        Raises:
            ValueError: Se medicamento não existir ou dados inválidos
        """
        # 1. Validar quantidade
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero!")
        
        # 2. Buscar medicamento
        medicamento = self.medicamento_repo.buscar_por_id(medicamento_id)
        if not medicamento:
            raise ValueError(f"Medicamento {medicamento_id} não encontrado!")
        
        # 3. Converter datas
        try:
            data_fab = datetime.strptime(data_fabricacao, "%Y-%m-%d").date()
            data_val = datetime.strptime(data_validade, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Formato de data inválido: {str(e)}")
        
        # 4. Validar datas
        if data_val <= data_fab:
            raise ValueError("Data de validade deve ser posterior à fabricação!")
        
        if data_val <= datetime.now().date():
            raise ValueError("Data de validade deve ser futura!")
        
        # 5. Criar novo lote
        lote = Lote(
            numero_lote=numero_lote,
            medicamento_id=medicamento_id,
            quantidade=quantidade,
            data_fabricacao=data_fab,
            data_validade=data_val,
            fornecedor=fornecedor
        )
        
        # 6. Salvar lote
        lote_salvo = self.lote_repo.salvar(lote)
        
        # 7. Calcular estoque total atualizado
        todos_lotes = self.lote_repo.buscar_por_medicamento(medicamento_id)
        estoque_total = sum(lote.quantidade for lote in todos_lotes)
        
        # 8. Determinar status
        if estoque_total < medicamento.estoque_minimo:
            status = "ATENCAO"
            mensagem = f"Estoque ainda abaixo do mínimo ({medicamento.estoque_minimo})"
        else:
            status = "OK"
            mensagem = "Estoque adequado"
        
        # 9. Retornar resultado
        return {
            "medicamento_id": medicamento.id,
            "medicamento_nome": medicamento.nome,
            "lote_adicionado": {
                "id": lote_salvo.id,
                "numero_lote": lote_salvo.numero_lote,
                "quantidade": lote_salvo.quantidade
            },
            "estoque_atual": estoque_total,
            "estoque_minimo": medicamento.estoque_minimo,
            "status": status,
            "mensagem": mensagem
        }
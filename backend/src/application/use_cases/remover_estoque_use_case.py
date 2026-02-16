"""
Use Case: Remover Estoque
Responsável por remover produtos do estoque (saída)
"""

from datetime import datetime
from typing import Dict, Any

from src.domain.ports import (
    MedicamentoRepositoryPort,
    LoteRepositoryPort
)


class RemoverEstoqueUseCase:
    """
    Use Case para remover estoque
    
    Fluxo:
    1. Valida se medicamento existe
    2. Verifica se tem estoque suficiente
    3. Remove quantidade dos lotes (FIFO - primeiro que vence sai primeiro)
    4. Atualiza lotes no banco
    5. Retorna informações atualizadas do estoque
    
    Regras de Negócio:
    - Quantidade deve ser maior que zero
    - Não pode remover mais do que tem em estoque
    - Estoque nunca fica negativo
    - Remove dos lotes mais antigos primeiro (FIFO)
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
        motivo: str,
        observacao: str = None
    ) -> Dict[str, Any]:
        """
        Executa o caso de uso
        
        Args:
            medicamento_id: ID do medicamento
            quantidade: Quantidade a remover
            motivo: Motivo da remoção (VENDA, VALIDADE, PERDA, etc)
            observacao: Observação adicional (opcional)
            
        Returns:
            Dicionário com informações do estoque atualizado
            
        Raises:
            ValueError: Se medicamento não existir ou estoque insuficiente
        """
        # 1. Validar quantidade
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero!")
        
        # 2. Buscar medicamento
        medicamento = self.medicamento_repo.buscar_por_id(medicamento_id)
        if not medicamento:
            raise ValueError(f"Medicamento {medicamento_id} não encontrado!")
        
        # 3. Buscar lotes do medicamento (ordenar por data de validade)
        lotes = self.lote_repo.buscar_por_medicamento(medicamento_id)
        
        # Filtrar apenas lotes não vencidos e com quantidade
        lotes_disponiveis = [
            lote for lote in lotes
            if lote.quantidade > 0 and lote.data_validade > datetime.now().date()
        ]
        
        # Ordenar por data de validade (FIFO - primeiro que vence sai primeiro)
        lotes_disponiveis.sort(key=lambda x: x.data_validade)
        
        # 4. Calcular estoque disponível
        estoque_disponivel = sum(lote.quantidade for lote in lotes_disponiveis)
        
        # 5. Validar se tem estoque suficiente
        if estoque_disponivel < quantidade:
            raise ValueError(
                f"Estoque insuficiente! Disponível: {estoque_disponivel}, "
                f"Solicitado: {quantidade}"
            )
        
        # 6. Remover quantidade dos lotes (FIFO)
        quantidade_restante = quantidade
        lotes_atualizados = []
        
        for lote in lotes_disponiveis:
            if quantidade_restante == 0:
                break
            
            # Quanto pode remover deste lote?
            quantidade_remover = min(quantidade_restante, lote.quantidade)
            
            # Atualizar quantidade do lote
            lote.quantidade -= quantidade_remover
            
            # Salvar lote atualizado
            lote_atualizado = self.lote_repo.atualizar(lote)
            lotes_atualizados.append({
                "lote_id": lote_atualizado.id,
                "numero_lote": lote_atualizado.numero_lote,
                "quantidade_removida": quantidade_remover,
                "quantidade_restante": lote_atualizado.quantidade
            })
            
            quantidade_restante -= quantidade_remover
        
        # 7. Calcular estoque total atualizado
        todos_lotes = self.lote_repo.buscar_por_medicamento(medicamento_id)
        estoque_total = sum(
            lote.quantidade for lote in todos_lotes
            if lote.data_validade > datetime.now().date()
        )
        
        # 8. Determinar status
        if estoque_total == 0:
            status = "CRITICO"
            mensagem = "Estoque zerado! Necessário repor urgentemente!"
        elif estoque_total < medicamento.estoque_minimo:
            status = "ATENCAO"
            mensagem = f"Estoque abaixo do mínimo ({medicamento.estoque_minimo})"
        else:
            status = "OK"
            mensagem = "Estoque adequado"
        
        # 9. Retornar resultado
        return {
            "medicamento_id": medicamento.id,
            "medicamento_nome": medicamento.nome,
            "motivo": motivo,
            "observacao": observacao,
            "quantidade_removida": quantidade,
            "lotes_afetados": lotes_atualizados,
            "estoque_atual": estoque_total,
            "estoque_minimo": medicamento.estoque_minimo,
            "status": status,
            "mensagem": mensagem
        }
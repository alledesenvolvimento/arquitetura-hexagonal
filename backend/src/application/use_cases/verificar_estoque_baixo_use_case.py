"""
Use Case: Verificar Estoque Baixo
Responsável por identificar medicamentos com estoque crítico
"""

from datetime import datetime
from typing import List, Dict, Any

from src.domain.ports import (
    MedicamentoRepositoryPort,
    LoteRepositoryPort
)


class VerificarEstoqueBaixoUseCase:
    """
    Use Case para verificar estoque baixo
    
    Fluxo:
    1. Lista todos os medicamentos
    2. Para cada medicamento, calcula estoque disponível
    3. Compara com estoque mínimo
    4. Retorna lista de medicamentos em alerta
    
    Regras de Negócio:
    - Considera apenas lotes não vencidos
    - CRÍTICO: estoque = 0
    - ATENÇÃO: estoque < mínimo
    - OK: estoque >= mínimo
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
    
    def execute(self) -> List[Dict[str, Any]]:
        """
        Executa o caso de uso
        
        Returns:
            Lista de medicamentos com estoque baixo/crítico
        """
        # 1. Buscar todos os medicamentos
        medicamentos = self.medicamento_repo.listar_todos()
        
        # 2. Lista para armazenar alertas
        alertas = []
        
        # 3. Verificar cada medicamento
        for medicamento in medicamentos:
            # Buscar lotes do medicamento
            lotes = self.lote_repo.buscar_por_medicamento(medicamento.id)
            
            # Calcular estoque disponível (apenas lotes não vencidos)
            estoque_disponivel = sum(
                lote.quantidade for lote in lotes
                if lote.data_validade > datetime.now().date()
            )
            
            # Verificar se está abaixo do mínimo ou zerado
            if estoque_disponivel == 0:
                # CRÍTICO - zerado!
                alertas.append({
                    "medicamento_id": medicamento.id,
                    "nome": medicamento.nome,
                    "principio_ativo": medicamento.principio_ativo,
                    "estoque_atual": estoque_disponivel,
                    "estoque_minimo": medicamento.estoque_minimo,
                    "diferenca": medicamento.estoque_minimo - estoque_disponivel,
                    "status": "CRITICO",
                    "prioridade": 1  # Máxima prioridade
                })
            elif estoque_disponivel < medicamento.estoque_minimo:
                # ATENÇÃO - abaixo do mínimo
                alertas.append({
                    "medicamento_id": medicamento.id,
                    "nome": medicamento.nome,
                    "principio_ativo": medicamento.principio_ativo,
                    "estoque_atual": estoque_disponivel,
                    "estoque_minimo": medicamento.estoque_minimo,
                    "diferenca": medicamento.estoque_minimo - estoque_disponivel,
                    "status": "ATENCAO",
                    "prioridade": 2  # Alta prioridade
                })
        
        # 4. Ordenar por prioridade (crítico primeiro) e depois por diferença
        alertas.sort(key=lambda x: (x["prioridade"], -x["diferenca"]))
        
        return alertas
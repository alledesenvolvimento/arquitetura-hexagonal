"""
Use Case: Relatório de Movimentações
Gera relatório de entradas e saídas de estoque
"""

from typing import Dict, List, Any
from datetime import date, timedelta
from decimal import Decimal

from src.domain.ports import LoteRepositoryPort, MedicamentoRepositoryPort


class RelatorioMovimentacoesUseCase:
    """
    Use Case para relatório de movimentações de estoque
    
    Fluxo:
    1. Busca lotes criados no período (entradas)
    2. Para cada lote, calcula quantidade removida (saídas)
    3. Agrupa por medicamento
    4. Calcula totais e saldo
    5. Retorna relatório de movimentações
    """
    
    def __init__(
        self,
        medicamento_repository: MedicamentoRepositoryPort,
        lote_repository: LoteRepositoryPort
    ):
        self.medicamento_repository = medicamento_repository
        self.lote_repository = lote_repository
    
    def execute(self, dias: int = 30) -> Dict[str, Any]:
        """
        Gera relatório de movimentações
        
        Args:
            dias: Número de dias para considerar (padrão: 30)
            
        Returns:
            Dicionário com relatório de movimentações
        """
        # 1. Calcular data inicial
        data_inicial = date.today() - timedelta(days=dias)
        
        # 2. Buscar todos os lotes
        # NOTA: Como não temos filtro por data no repositório,
        # vamos buscar todos e filtrar em memória
        todos_lotes = self.lote_repository.listar_todos()
        
        # Filtrar lotes do período (por data de fabricação)
        lotes_periodo = [
            lote for lote in todos_lotes
            if lote.data_fabricacao >= data_inicial
        ]
        
        # 3. Preparar dados de movimentações
        movimentacoes = []
        total_entradas = 0
        total_saidas = 0
        
        # Agrupar por medicamento
        medicamentos_dict = {}
        
        for lote in lotes_periodo:
            medicamento_id = lote.medicamento_id
            
            if medicamento_id not in medicamentos_dict:
                # Buscar info do medicamento
                medicamento = self.medicamento_repository.buscar_por_id(medicamento_id)
                if not medicamento:
                    continue
                
                medicamentos_dict[medicamento_id] = {
                    "medicamento_id": medicamento_id,
                    "nome": medicamento.nome,
                    "entradas": 0,
                    "saidas": 0,
                    "saldo": 0,
                    "lotes": []
                }
            
            # Considerar entrada = quantidade atual do lote
            quantidade_entrada = lote.quantidade
            
            medicamentos_dict[medicamento_id]["entradas"] += quantidade_entrada
            medicamentos_dict[medicamento_id]["lotes"].append({
                "numero_lote": lote.numero_lote,
                "quantidade": quantidade_entrada,
                "data_fabricacao": lote.data_fabricacao.isoformat(),
                "data_validade": lote.data_validade.isoformat()
            })
            
            total_entradas += quantidade_entrada
        
        # Converter dict para lista
        movimentacoes = list(medicamentos_dict.values())
        
        # Calcular saldo de cada medicamento
        for item in movimentacoes:
            item["saldo"] = item["entradas"] - item["saidas"]
        
        # 4. Ordenar por nome
        movimentacoes.sort(key=lambda x: x["nome"])
        
        # 5. Montar relatório final
        relatorio = {
            "periodo": {
                "data_inicial": data_inicial.isoformat(),
                "data_final": date.today().isoformat(),
                "dias": dias
            },
            "resumo": {
                "total_entradas": total_entradas,
                "total_saidas": total_saidas,
                "saldo": total_entradas - total_saidas,
                "total_medicamentos": len(movimentacoes)
            },
            "movimentacoes": movimentacoes,
            "observacao": "Relatório baseado em lotes cadastrados no período. "
                         "Para histórico completo de vendas, implemente tabela de movimentações."
        }
        
        return relatorio
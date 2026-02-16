"""
Use Case: Monitorar Produtos Vencendo
Verifica produtos vencendo E dispara eventos! 📢
"""

from typing import Dict, Any
from datetime import date, timedelta

from src.domain.ports import MedicamentoRepositoryPort, LoteRepositoryPort
from src.domain.events import ProdutoVencendoEvent
from src.domain.events.event_dispatcher import event_dispatcher


class MonitorarProdutosVencendoUseCase:
    """
    Use Case para monitorar produtos vencendo
    
    Usa Observer Pattern pra notificar! 📢
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
        Monitora produtos que vão vencer nos próximos N dias
        
        Args:
            dias: Número de dias pra frente (padrão: 30)
            
        Returns:
            Lista de produtos vencendo
        """
        # 1. Calcular data limite
        hoje = date.today()
        data_limite = hoje + timedelta(days=dias)
        
        # 2. Buscar todos os lotes
        todos_lotes = self.lote_repository.listar_todos()
        
        # 3. Filtrar lotes que vão vencer
        lotes_vencendo = []
        
        for lote in todos_lotes:
            # Pular lotes já vencidos
            if lote.data_validade <= hoje:
                continue
            
            # Verificar se vence no período
            if lote.data_validade <= data_limite:
                # Calcular dias até vencer
                dias_ate_vencer = (lote.data_validade - hoje).days
                
                # Buscar info do medicamento
                medicamento = self.medicamento_repository.buscar_por_id(
                    lote.medicamento_id
                )
                
                if not medicamento:
                    continue
                
                # 🔥 DISPARAR EVENTO! (Observer Pattern)
                evento = ProdutoVencendoEvent(
                    medicamento_id=medicamento.id,
                    nome_medicamento=medicamento.nome,
                    lote_id=lote.id,
                    numero_lote=lote.numero_lote,
                    data_validade=lote.data_validade.isoformat(),
                    dias_ate_vencer=dias_ate_vencer,
                    quantidade=lote.quantidade
                )
                event_dispatcher.notificar(evento)
                
                # Adicionar na lista de retorno
                lotes_vencendo.append({
                    "medicamento": {
                        "id": medicamento.id,
                        "nome": medicamento.nome,
                        "principio_ativo": medicamento.principio_ativo
                    },
                    "lote": {
                        "id": lote.id,
                        "numero_lote": lote.numero_lote,
                        "quantidade": lote.quantidade,
                        "data_validade": lote.data_validade.isoformat(),
                        "dias_ate_vencer": dias_ate_vencer
                    },
                    "urgencia": "CRITICO" if dias_ate_vencer <= 7 else "ATENCAO"
                })
        
        # 4. Ordenar por urgência (menos dias primeiro)
        lotes_vencendo.sort(key=lambda x: x["lote"]["dias_ate_vencer"])
        
        # 5. Retornar resultado
        return {
            "periodo_monitorado_dias": dias,
            "total_lotes_vencendo": len(lotes_vencendo),
            "lotes": lotes_vencendo,
            "eventos_disparados": len(lotes_vencendo)
        }
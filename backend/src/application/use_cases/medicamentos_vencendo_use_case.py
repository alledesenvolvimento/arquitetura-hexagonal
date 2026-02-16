"""
Use Case: Medicamentos Vencendo
Lista medicamentos que estão próximos da data de validade
"""

from typing import Dict, List, Any
from datetime import date, timedelta

from src.domain.ports import LoteRepositoryPort, MedicamentoRepositoryPort


class MedicamentosVencendoUseCase:
    """
    Use Case para listar medicamentos vencendo
    
    Fluxo:
    1. Busca todos os lotes
    2. Filtra lotes que vencem nos próximos N dias
    3. Agrupa por medicamento
    4. Calcula dias restantes e prioridade
    5. Retorna lista ordenada por urgência
    """
    
    def __init__(
        self,
        medicamento_repository: MedicamentoRepositoryPort,
        lote_repository: LoteRepositoryPort
    ):
        self.medicamento_repository = medicamento_repository
        self.lote_repository = lote_repository
    
    def execute(self, dias: int = 60) -> Dict[str, Any]:
        """
        Lista medicamentos vencendo
        
        Args:
            dias: Número de dias para alertar (padrão: 60)
            
        Returns:
            Dicionário com produtos vencendo
        """
        # 1. Calcular data limite
        data_limite = date.today() + timedelta(days=dias)
        
        # 2. Buscar lotes que vencem no período
        lotes_vencendo = self.lote_repository.listar_vencendo_em(dias)
        
        # 3. Agrupar por medicamento
        medicamentos_dict = {}
        
        for lote in lotes_vencendo:
            medicamento_id = lote.medicamento_id
            
            if medicamento_id not in medicamentos_dict:
                # Buscar info do medicamento
                medicamento = self.medicamento_repository.buscar_por_id(medicamento_id)
                if not medicamento:
                    continue
                
                medicamentos_dict[medicamento_id] = {
                    "medicamento_id": medicamento_id,
                    "nome": medicamento.nome,
                    "principio_ativo": medicamento.principio_ativo,
                    "preco_unitario": float(medicamento.preco),
                    "lotes": [],
                    "quantidade_total": 0,
                    "valor_total": 0,
                    "dias_ate_primeiro_vencimento": None
                }
            
            # Calcular dias até vencimento
            dias_restantes = (lote.data_validade - date.today()).days
            
            # Atualizar dias até primeiro vencimento
            if (medicamentos_dict[medicamento_id]["dias_ate_primeiro_vencimento"] is None or
                dias_restantes < medicamentos_dict[medicamento_id]["dias_ate_primeiro_vencimento"]):
                medicamentos_dict[medicamento_id]["dias_ate_primeiro_vencimento"] = dias_restantes
            
            # Calcular valor do lote
            medicamento = self.medicamento_repository.buscar_por_id(medicamento_id)
            valor_lote = medicamento.preco * lote.quantidade if medicamento else 0
            
            # Adicionar lote
            medicamentos_dict[medicamento_id]["lotes"].append({
                "numero_lote": lote.numero_lote,
                "quantidade": lote.quantidade,
                "data_validade": lote.data_validade.isoformat(),
                "dias_restantes": dias_restantes,
                "urgencia": self._classificar_urgencia(dias_restantes)
            })
            
            medicamentos_dict[medicamento_id]["quantidade_total"] += lote.quantidade
            medicamentos_dict[medicamento_id]["valor_total"] += float(valor_lote)
        
        # 4. Converter para lista
        produtos_vencendo = list(medicamentos_dict.values())
        
        # 5. Classificar urgência de cada produto
        for produto in produtos_vencendo:
            dias_restantes = produto["dias_ate_primeiro_vencimento"]
            produto["urgencia"] = self._classificar_urgencia(dias_restantes)
            produto["prioridade"] = self._calcular_prioridade(dias_restantes)
            produto["acao_sugerida"] = self._sugerir_acao(dias_restantes, produto["quantidade_total"])
        
        # 6. Ordenar por prioridade (mais urgente primeiro)
        produtos_vencendo.sort(key=lambda x: x["prioridade"])
        
        # 7. Calcular estatísticas
        if produtos_vencendo:
            quantidade_total = sum(p["quantidade_total"] for p in produtos_vencendo)
            valor_total = sum(p["valor_total"] for p in produtos_vencendo)
            
            # Contar por urgência
            urgencia_critica = sum(1 for p in produtos_vencendo if p["urgencia"] == "CRITICA")
            urgencia_alta = sum(1 for p in produtos_vencendo if p["urgencia"] == "ALTA")
            urgencia_media = sum(1 for p in produtos_vencendo if p["urgencia"] == "MEDIA")
        else:
            quantidade_total = 0
            valor_total = 0
            urgencia_critica = 0
            urgencia_alta = 0
            urgencia_media = 0
        
        # 8. Montar relatório final
        relatorio = {
            "periodo_analise": {
                "data_consulta": date.today().isoformat(),
                "dias_analisados": dias,
                "data_limite": data_limite.isoformat()
            },
            "resumo": {
                "total_produtos": len(produtos_vencendo),
                "quantidade_total": quantidade_total,
                "valor_total_risco": valor_total,
                "por_urgencia": {
                    "critica": urgencia_critica,
                    "alta": urgencia_alta,
                    "media": urgencia_media
                }
            },
            "produtos": produtos_vencendo,
            "alertas": self._gerar_alertas_gerenciais(
                urgencia_critica,
                urgencia_alta,
                valor_total
            )
        }
        
        return relatorio
    
    def _classificar_urgencia(self, dias_restantes: int) -> str:
        """Classifica urgência baseado nos dias restantes"""
        if dias_restantes <= 15:
            return "CRITICA"
        elif dias_restantes <= 30:
            return "ALTA"
        else:
            return "MEDIA"
    
    def _calcular_prioridade(self, dias_restantes: int) -> int:
        """Calcula prioridade numérica (menor = mais urgente)"""
        if dias_restantes <= 15:
            return 1
        elif dias_restantes <= 30:
            return 2
        else:
            return 3
    
    def _sugerir_acao(self, dias_restantes: int, quantidade: int) -> str:
        """Sugere ação baseado na urgência"""
        if dias_restantes <= 15:
            return f"🚨 URGENTE: Fazer promoção agressiva! {quantidade} unidades em risco"
        elif dias_restantes <= 30:
            return f"⚠️ Fazer promoção ou desconto. {quantidade} unidades precisam sair"
        else:
            return f"📋 Monitorar. {quantidade} unidades ainda têm tempo"
    
    def _gerar_alertas_gerenciais(
        self,
        urgencia_critica: int,
        urgencia_alta: int,
        valor_total: float
    ) -> List[Dict[str, str]]:
        """Gera alertas para o gerente"""
        alertas = []
        
        if urgencia_critica > 0:
            alertas.append({
                "tipo": "CRITICO",
                "mensagem": f"{urgencia_critica} produto(s) com vencimento CRÍTICO (≤15 dias)",
                "acao": "Ação imediata: Promoções agressivas, doação ou descarte planejado"
            })
        
        if urgencia_alta > 0:
            alertas.append({
                "tipo": "ATENCAO",
                "mensagem": f"{urgencia_alta} produto(s) vencem em até 30 dias",
                "acao": "Planejar promoções e aumentar divulgação"
            })
        
        if valor_total > 1000:
            alertas.append({
                "tipo": "FINANCEIRO",
                "mensagem": f"R$ {valor_total:.2f} em risco de perda por vencimento",
                "acao": "Priorizar venda destes produtos para evitar prejuízo"
            })
        
        if len(alertas) == 0:
            alertas.append({
                "tipo": "OK",
                "mensagem": "Nenhum produto com vencimento crítico no período",
                "acao": "Continuar monitoramento regular"
            })
        
        return alertas
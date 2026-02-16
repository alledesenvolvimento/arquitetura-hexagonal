"""
Use Case: Relatório de Estoque
Gera relatório completo do estoque atual da farmácia
"""

from typing import Dict, List, Any
from decimal import Decimal

from src.domain.ports import MedicamentoRepositoryPort, LoteRepositoryPort


class RelatorioEstoqueUseCase:
    """
    Use Case para gerar relatório de estoque
    
    Fluxo:
    1. Busca todos os medicamentos
    2. Para cada medicamento, busca seus lotes
    3. Calcula totais e estatísticas
    4. Identifica alertas (estoque baixo, produtos vencendo)
    5. Retorna relatório consolidado
    """
    
    def __init__(
        self,
        medicamento_repository: MedicamentoRepositoryPort,
        lote_repository: LoteRepositoryPort
    ):
        self.medicamento_repository = medicamento_repository
        self.lote_repository = lote_repository
    
    def execute(self, incluir_zerados: bool = False) -> Dict[str, Any]:
        """
        Gera relatório de estoque
        
        Args:
            incluir_zerados: Se deve incluir produtos com estoque zero
            
        Returns:
            Dicionário com relatório completo
        """
        # 1. Buscar todos os medicamentos
        medicamentos = self.medicamento_repository.listar_todos()
        
        # 2. Preparar dados do relatório
        itens_estoque = []
        total_produtos = 0
        total_unidades = 0
        valor_total = Decimal("0")
        produtos_abaixo_minimo = 0
        produtos_zerados = 0
        
        for medicamento in medicamentos:
            # Buscar lotes do medicamento
            lotes = self.lote_repository.buscar_por_medicamento(medicamento.id)
            
            # Calcular estoque disponível (só lotes não vencidos)
            from datetime import date
            estoque_disponivel = sum(
                lote.quantidade 
                for lote in lotes 
                if lote.data_validade > date.today()
            )
            
            # Pular produtos zerados se não deve incluir
            if not incluir_zerados and estoque_disponivel == 0:
                produtos_zerados += 1
                continue
            
            # Verificar status
            if estoque_disponivel == 0:
                status = "ZERADO"
                prioridade = 1
                produtos_zerados += 1
            elif estoque_disponivel < medicamento.estoque_minimo:
                status = "ABAIXO_MINIMO"
                prioridade = 2
                produtos_abaixo_minimo += 1
            else:
                status = "OK"
                prioridade = 3
            
            # Calcular valor em estoque
            valor_estoque = medicamento.preco * estoque_disponivel
            
            # Adicionar item ao relatório
            item = {
                "medicamento_id": medicamento.id,
                "nome": medicamento.nome,
                "principio_ativo": medicamento.principio_ativo,
                "preco_unitario": float(medicamento.preco),
                "estoque_atual": estoque_disponivel,
                "estoque_minimo": medicamento.estoque_minimo,
                "status": status,
                "prioridade": prioridade,
                "valor_em_estoque": float(valor_estoque),
                "total_lotes": len(lotes)
            }
            
            itens_estoque.append(item)
            
            # Atualizar totalizadores
            total_produtos += 1
            total_unidades += estoque_disponivel
            valor_total += valor_estoque
        
        # 3. Ordenar por prioridade (críticos primeiro)
        itens_estoque.sort(key=lambda x: (x["prioridade"], x["nome"]))
        
        # 4. Montar relatório final
        relatorio = {
            "resumo": {
                "total_produtos": total_produtos,
                "total_unidades": total_unidades,
                "valor_total_estoque": float(valor_total),
                "produtos_abaixo_minimo": produtos_abaixo_minimo,
                "produtos_zerados": produtos_zerados,
                "produtos_ok": total_produtos - produtos_abaixo_minimo - produtos_zerados
            },
            "itens": itens_estoque,
            "alertas": self._gerar_alertas(
                produtos_abaixo_minimo,
                produtos_zerados,
                itens_estoque
            )
        }
        
        return relatorio
    
    def _gerar_alertas(
        self,
        produtos_abaixo_minimo: int,
        produtos_zerados: int,
        itens: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Gera lista de alertas baseado no estoque"""
        alertas = []
        
        # Alerta de produtos zerados
        if produtos_zerados > 0:
            produtos_nomes = [
                item["nome"] 
                for item in itens 
                if item["status"] == "ZERADO"
            ][:3]  # Até 3 produtos
            
            alertas.append({
                "tipo": "CRITICO",
                "mensagem": f"{produtos_zerados} produto(s) com estoque ZERADO!",
                "produtos": produtos_nomes,
                "acao": "Urgente: Solicitar reposição imediata"
            })
        
        # Alerta de produtos abaixo do mínimo
        if produtos_abaixo_minimo > 0:
            produtos_nomes = [
                item["nome"] 
                for item in itens 
                if item["status"] == "ABAIXO_MINIMO"
            ][:3]  # Até 3 produtos
            
            alertas.append({
                "tipo": "ATENCAO",
                "mensagem": f"{produtos_abaixo_minimo} produto(s) abaixo do estoque mínimo",
                "produtos": produtos_nomes,
                "acao": "Programar pedido de reposição"
            })
        
        # Alerta se tudo ok
        if len(alertas) == 0:
            alertas.append({
                "tipo": "OK",
                "mensagem": "Estoque em situação normal",
                "produtos": [],
                "acao": "Continuar monitoramento"
            })
        
        return alertas
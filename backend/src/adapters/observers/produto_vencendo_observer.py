"""
Observer: Produto Vencendo
Reage quando produto está perto de vencer
"""

from src.domain.events import ProdutoVencendoEvent
from .base_observer import BaseObserver


class ProdutoVencendoObserver(BaseObserver):
    """
    Observer que reage a produtos vencendo
    
    Ações:
    - Imprime alerta no console (agora)
    - Poderia marcar pra promoção (futuro)
    - Poderia avisar vendedores (futuro)
    - Poderia criar desconto automático (futuro)
    """
    
    def __init__(self, dias_alerta_critico: int = 7):
        """
        Args:
            dias_alerta_critico: Dias pra considerar crítico
        """
        self.dias_alerta_critico = dias_alerta_critico
    
    def notificar(self, evento: ProdutoVencendoEvent):
        """
        Reage ao evento de produto vencendo
        
        Args:
            evento: ProdutoVencendoEvent com dados
        """
        # Determinar urgência
        if evento.dias_ate_vencer <= self.dias_alerta_critico:
            nivel = "🚨 CRÍTICO"
            acao = "PROMOÇÃO URGENTE ou DESCARTE"
        elif evento.dias_ate_vencer <= 15:
            nivel = "⚠️ URGENTE"
            acao = "Fazer promoção"
        else:
            nivel = "⚡ ATENÇÃO"
            acao = "Monitorar de perto"
        
        # Imprimir alerta
        print("\n" + "="*60)
        print(f"{nivel} - PRODUTO VENCENDO!")
        print("="*60)
        print(f"💊 Produto: {evento.nome_medicamento}")
        print(f"📦 Lote: {evento.numero_lote}")
        print(f"📅 Validade: {evento.data_validade}")
        print(f"⏰ Vence em: {evento.dias_ate_vencer} dias")
        print(f"📊 Quantidade: {evento.quantidade} unidades")
        print(f"⏰ Quando: {evento.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*60)
        print(f"💡 AÇÃO SUGERIDA: {acao}")
        
        # Se crítico, dar sugestão de desconto
        if evento.dias_ate_vencer <= self.dias_alerta_critico:
            desconto_sugerido = min(50, evento.dias_ate_vencer * 5)
            print(f"💰 DESCONTO SUGERIDO: {desconto_sugerido}% OFF")
        
        print("="*60 + "\n")
        
        # Aqui você poderia:
        # - Criar promoção automática
        # - Avisar vendedores
        # - Marcar no sistema
    
    # Métodos futuros (comentados por enquanto)
    # def _criar_promocao(self, evento):
    #     """Cria promoção automática"""
    #     pass
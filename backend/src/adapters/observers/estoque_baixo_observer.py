"""
Observer: Estoque Baixo
Reage quando estoque fica crítico
"""

from src.domain.events import EstoqueBaixoEvent
from .base_observer import BaseObserver


class EstoqueBaixoObserver(BaseObserver):
    """
    Observer que reage a estoque baixo
    
    Ações:
    - Imprime alerta no console (agora)
    - Poderia enviar email pro gerente (futuro)
    - Poderia criar notificação no app (futuro)
    - Poderia enviar SMS (futuro)
    """
    
    def __init__(self, nome_gerente: str = "Gerente"):
        self.nome_gerente = nome_gerente
    
    def notificar(self, evento: EstoqueBaixoEvent):
        """
        Reage ao evento de estoque baixo
        
        Args:
            evento: EstoqueBaixoEvent com dados do estoque
        """
        # Extrair dados do evento
        dados = evento.to_dict()
        
        # Calcular urgência
        diferenca = evento.estoque_minimo - evento.estoque_atual
        percentual = (evento.estoque_atual / evento.estoque_minimo) * 100
        
        # Determinar nível de alerta
        if percentual <= 20:
            nivel = "🚨 CRÍTICO"
        elif percentual <= 50:
            nivel = "⚠️ URGENTE"
        else:
            nivel = "⚡ ATENÇÃO"
        
        # Imprimir alerta
        print("\n" + "="*60)
        print(f"{nivel} - ESTOQUE BAIXO DETECTADO!")
        print("="*60)
        print(f"📦 Produto: {evento.nome_medicamento}")
        print(f"📊 Estoque atual: {evento.estoque_atual} unidades")
        print(f"📊 Estoque mínimo: {evento.estoque_minimo} unidades")
        print(f"📉 Faltam: {diferenca} unidades")
        print(f"📊 Nível: {percentual:.1f}% do mínimo")
        print(f"👤 Notificando: {self.nome_gerente}")
        print(f"⏰ Quando: {evento.timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*60)
        print("💡 AÇÃO SUGERIDA: Solicitar reposição imediata!")
        print("="*60 + "\n")
        
        # Aqui você poderia:
        # - Enviar email: self._enviar_email(evento)
        # - Enviar SMS: self._enviar_sms(evento)
        # - Criar tarefa: self._criar_tarefa(evento)
    
    # Métodos futuros (comentados por enquanto)
    # def _enviar_email(self, evento):
    #     """Envia email pro gerente"""
    #     pass
    # 
    # def _enviar_sms(self, evento):
    #     """Envia SMS pro gerente"""
    #     pass
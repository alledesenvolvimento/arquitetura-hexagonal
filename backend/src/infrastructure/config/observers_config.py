"""
Configuração de Observers
Registra observers no event dispatcher
"""

from src.domain.events import EstoqueBaixoEvent, ProdutoVencendoEvent
from src.domain.events.event_dispatcher import event_dispatcher
from src.adapters.observers import (
    EstoqueBaixoObserver,
    ProdutoVencendoObserver
)


def configurar_observers():
    """
    Registra todos os observers no sistema
    
    Chamado na inicialização da aplicação
    """
    print("\n🔧 Configurando observers...")
    
    # 1. Criar instâncias dos observers
    estoque_baixo_obs = EstoqueBaixoObserver(nome_gerente="Gerente AlleFarma")
    produto_vencendo_obs = ProdutoVencendoObserver(dias_alerta_critico=7)
    
    # 2. Registrar observers
    event_dispatcher.registrar(EstoqueBaixoEvent, estoque_baixo_obs)
    event_dispatcher.registrar(ProdutoVencendoEvent, produto_vencendo_obs)
    
    # 3. Confirmar
    observers_registrados = event_dispatcher.listar_observers()
    print(f"✅ Observers configurados: {observers_registrados}")
    print()


def limpar_observers():
    """
    Limpa todos os observers
    
    Útil pra testes
    """
    event_dispatcher.limpar()
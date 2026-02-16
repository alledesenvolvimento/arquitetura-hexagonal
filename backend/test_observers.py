"""
Testes: Observer Pattern
Testa eventos e observers
Aula 12 - Design Patterns
"""

from src.domain.events import EstoqueBaixoEvent, ProdutoVencendoEvent
from src.domain.events.event_dispatcher import EventDispatcher
from src.adapters.observers import (
    EstoqueBaixoObserver,
    ProdutoVencendoObserver
)


def teste_evento_estoque_baixo():
    """Testa criação e serialização do evento"""
    print("\n🧪 Teste 1: Evento de estoque baixo")
    
    evento = EstoqueBaixoEvent(
        medicamento_id=1,
        nome_medicamento="Dipirona",
        estoque_atual=10,
        estoque_minimo=50
    )
    
    dados = evento.to_dict()
    
    assert dados["tipo"] == "EstoqueBaixoEvent"
    assert dados["dados"]["medicamento_id"] == 1
    assert dados["dados"]["diferenca"] == 40
    
    print("✅ Evento criado e serializado com sucesso!")
    print(f"   Tipo: {dados['tipo']}")
    print(f"   Diferença: {dados['dados']['diferenca']} unidades")


def teste_registrar_observer():
    """Testa registro de observer"""
    print("\n🧪 Teste 2: Registrar observer")
    
    dispatcher = EventDispatcher()
    dispatcher.limpar()
    
    observer = EstoqueBaixoObserver()
    dispatcher.registrar(EstoqueBaixoEvent, observer)
    
    observers = dispatcher.listar_observers()
    
    assert "EstoqueBaixoEvent" in observers
    assert len(observers["EstoqueBaixoEvent"]) == 1
    
    print("✅ Observer registrado com sucesso!")
    print(f"   Observers registrados: {list(observers.keys())}")


def teste_notificar_observer():
    """Testa notificação de observer"""
    print("\n🧪 Teste 3: Notificar observer")
    
    dispatcher = EventDispatcher()
    dispatcher.limpar()
    
    observer = EstoqueBaixoObserver(nome_gerente="João")
    dispatcher.registrar(EstoqueBaixoEvent, observer)
    
    evento = EstoqueBaixoEvent(
        medicamento_id=1,
        nome_medicamento="Dipirona",
        estoque_atual=5,
        estoque_minimo=50
    )
    
    print("   Disparando evento...")
    dispatcher.notificar(evento)
    
    print("✅ Observer notificado com sucesso!")


def teste_produto_vencendo_observer():
    """Testa observer de produto vencendo"""
    print("\n🧪 Teste 4: Observer de produto vencendo")
    
    dispatcher = EventDispatcher()
    dispatcher.limpar()
    
    observer = ProdutoVencendoObserver(dias_alerta_critico=7)
    dispatcher.registrar(ProdutoVencendoEvent, observer)
    
    evento = ProdutoVencendoEvent(
        medicamento_id=1,
        nome_medicamento="Rivotril",
        lote_id=1,
        numero_lote="LOT123",
        data_validade="2026-02-20",
        dias_ate_vencer=4,  # Crítico!
        quantidade=30
    )
    
    print("   Disparando evento...")
    dispatcher.notificar(evento)
    
    print("✅ Observer de produto vencendo funcionou!")


def teste_multiplos_observers():
    """Testa múltiplos observers pro mesmo evento"""
    print("\n🧪 Teste 5: Múltiplos observers")
    
    dispatcher = EventDispatcher()
    dispatcher.limpar()
    
    obs1 = EstoqueBaixoObserver(nome_gerente="Gerente 1")
    obs2 = EstoqueBaixoObserver(nome_gerente="Gerente 2")
    
    dispatcher.registrar(EstoqueBaixoEvent, obs1)
    dispatcher.registrar(EstoqueBaixoEvent, obs2)
    
    evento = EstoqueBaixoEvent(
        medicamento_id=1,
        nome_medicamento="Teste",
        estoque_atual=5,
        estoque_minimo=50
    )
    
    print("   Disparando evento para 2 observers...")
    dispatcher.notificar(evento)
    
    print("✅ Múltiplos observers notificados!")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO OBSERVER PATTERN (AULA 12)")
    print("=" * 60)
    
    teste_evento_estoque_baixo()
    teste_registrar_observer()
    teste_notificar_observer()
    teste_produto_vencendo_observer()
    teste_multiplos_observers()
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES DO OBSERVER PASSARAM!")
    print("=" * 60)
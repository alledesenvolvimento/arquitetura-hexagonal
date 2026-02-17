"""
Testes Unitários: Observer Pattern
Testa Eventos, EventDispatcher e Observers usando pytest

Aula 13 - Testes Unitários
"""

import pytest

from src.domain.events import EstoqueBaixoEvent, ProdutoVencendoEvent
from src.domain.events.event_dispatcher import EventDispatcher
from src.adapters.observers import (
    EstoqueBaixoObserver,
    ProdutoVencendoObserver
)


# ==========================================
# FIXTURE LOCAL - EventDispatcher limpo
# ==========================================

@pytest.fixture
def dispatcher_limpo():
    """Fixture: EventDispatcher limpo a cada teste"""
    dispatcher = EventDispatcher()
    dispatcher.limpar()
    return dispatcher


# ==========================================
# TESTES: EstoqueBaixoEvent
# ==========================================

class TestEstoqueBaixoEvent:
    """Testes para o evento de estoque baixo"""

    def test_criar_evento_estoque_baixo(self):
        """✅ Deve criar evento com dados válidos"""
        evento = EstoqueBaixoEvent(
            medicamento_id=1,
            nome_medicamento="Dipirona",
            estoque_atual=10,
            estoque_minimo=50
        )

        assert evento.medicamento_id == 1
        assert evento.nome_medicamento == "Dipirona"
        assert evento.estoque_atual == 10
        assert evento.estoque_minimo == 50

    def test_evento_serializa_para_dict(self):
        """✅ Deve serializar para dicionário corretamente"""
        evento = EstoqueBaixoEvent(
            medicamento_id=1,
            nome_medicamento="Dipirona",
            estoque_atual=10,
            estoque_minimo=50
        )

        dados = evento.to_dict()

        assert dados["tipo"] == "EstoqueBaixoEvent"
        assert dados["dados"]["medicamento_id"] == 1
        assert dados["dados"]["diferenca"] == 40  # 50 - 10 = 40!

    def test_evento_calcula_diferenca_corretamente(self):
        """✅ Deve calcular diferença (mínimo - atual) corretamente"""
        evento = EstoqueBaixoEvent(
            medicamento_id=1,
            nome_medicamento="Teste",
            estoque_atual=5,
            estoque_minimo=100
        )

        dados = evento.to_dict()

        assert dados["dados"]["diferenca"] == 95  # 100 - 5 = 95!


# ==========================================
# TESTES: ProdutoVencendoEvent
# ==========================================

class TestProdutoVencendoEvent:
    """Testes para o evento de produto vencendo"""

    def test_criar_evento_produto_vencendo(self):
        """✅ Deve criar evento com dados válidos"""
        evento = ProdutoVencendoEvent(
            medicamento_id=1,
            nome_medicamento="Rivotril",
            lote_id=1,
            numero_lote="LOT123",
            data_validade="2026-02-20",
            dias_ate_vencer=4,
            quantidade=30
        )

        assert evento.medicamento_id == 1
        assert evento.numero_lote == "LOT123"
        assert evento.dias_ate_vencer == 4

    def test_evento_produto_vencendo_serializa(self):
        """✅ Deve serializar para dicionário"""
        evento = ProdutoVencendoEvent(
            medicamento_id=1,
            nome_medicamento="Rivotril",
            lote_id=1,
            numero_lote="LOT123",
            data_validade="2026-02-20",
            dias_ate_vencer=4,
            quantidade=30
        )

        dados = evento.to_dict()

        assert dados["tipo"] == "ProdutoVencendoEvent"
        assert dados["dados"]["numero_lote"] == "LOT123"


# ==========================================
# TESTES: EventDispatcher
# ==========================================

class TestEventDispatcher:
    """Testes para o despachante de eventos"""

    def test_registrar_observer(self, dispatcher_limpo):
        """✅ Deve registrar observer para um evento"""
        observer = EstoqueBaixoObserver()
        dispatcher_limpo.registrar(EstoqueBaixoEvent, observer)

        observers = dispatcher_limpo.listar_observers()

        assert "EstoqueBaixoEvent" in observers
        assert len(observers["EstoqueBaixoEvent"]) == 1

    def test_registrar_multiplos_observers(self, dispatcher_limpo):
        """✅ Deve registrar múltiplos observers para o mesmo evento"""
        obs1 = EstoqueBaixoObserver(nome_gerente="Gerente 1")
        obs2 = EstoqueBaixoObserver(nome_gerente="Gerente 2")

        dispatcher_limpo.registrar(EstoqueBaixoEvent, obs1)
        dispatcher_limpo.registrar(EstoqueBaixoEvent, obs2)

        observers = dispatcher_limpo.listar_observers()

        assert len(observers["EstoqueBaixoEvent"]) == 2

    def test_notificar_observer_registrado(self, dispatcher_limpo):
        """✅ Observer registrado deve ser notificado"""
        notificacoes = []

        class ObserverTeste:
            def notificar(self, evento):
                notificacoes.append(evento)

        dispatcher_limpo.registrar(EstoqueBaixoEvent, ObserverTeste())

        evento = EstoqueBaixoEvent(
            medicamento_id=1,
            nome_medicamento="Dipirona",
            estoque_atual=5,
            estoque_minimo=50
        )
        dispatcher_limpo.notificar(evento)

        assert len(notificacoes) == 1
        assert notificacoes[0].medicamento_id == 1

    def test_nao_notifica_observer_de_outro_evento(self, dispatcher_limpo):
        """✅ Não deve notificar observers de outros tipos de evento"""
        notificacoes = []

        class ObserverTeste:
            def notificar(self, evento):
                notificacoes.append(evento)

        # Registra para EstoqueBaixoEvent
        dispatcher_limpo.registrar(EstoqueBaixoEvent, ObserverTeste())

        # Mas dispara ProdutoVencendoEvent
        evento = ProdutoVencendoEvent(
            medicamento_id=1,
            nome_medicamento="Teste",
            lote_id=1,
            numero_lote="LOT",
            data_validade="2026-12-31",
            dias_ate_vencer=30,
            quantidade=10
        )
        dispatcher_limpo.notificar(evento)

        # Observer de EstoqueBaixo NÃO deve ter sido notificado!
        assert len(notificacoes) == 0

    def test_limpar_remove_todos_observers(self, dispatcher_limpo):
        """✅ limpar() deve remover todos os observers"""
        dispatcher_limpo.registrar(EstoqueBaixoEvent, EstoqueBaixoObserver())
        dispatcher_limpo.registrar(ProdutoVencendoEvent, ProdutoVencendoObserver())

        dispatcher_limpo.limpar()

        observers = dispatcher_limpo.listar_observers()
        assert len(observers) == 0


# ==========================================
# TESTES: EstoqueBaixoObserver
# ==========================================

class TestEstoqueBaixoObserver:
    """Testes para o observer de estoque baixo"""

    def test_observer_criado_com_gerente_padrao(self):
        """✅ Deve ser criado com gerente padrão"""
        observer = EstoqueBaixoObserver()

        assert observer is not None

    def test_observer_criado_com_gerente_customizado(self):
        """✅ Deve ser criado com gerente customizado"""
        observer = EstoqueBaixoObserver(nome_gerente="João Silva")

        assert observer is not None

    def test_observer_processa_evento_sem_erro(self):
        """✅ Deve processar evento sem lançar exceção"""
        observer = EstoqueBaixoObserver(nome_gerente="Teste")

        evento = EstoqueBaixoEvent(
            medicamento_id=1,
            nome_medicamento="Dipirona",
            estoque_atual=5,
            estoque_minimo=50
        )

        # Não deve lançar exceção!
        observer.notificar(evento)
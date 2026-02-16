"""
Event Dispatcher
Responsável por notificar observers quando eventos acontecem
Observer Pattern - parte central
"""

from typing import Dict, List, Type
from .base_event import BaseEvent


class EventDispatcher:
    """
    Despachante de eventos (padrão Singleton)
    
    Responsabilidades:
    1. Guardar lista de observers registrados
    2. Notificar observers quando evento acontece
    3. Gerenciar registro/remoção de observers
    """
    
    _instance = None  # Singleton
    
    def __new__(cls):
        """Padrão Singleton - só 1 instância"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializa estruturas internas"""
        # Dicionário: TipoEvento -> Lista de Observers
        self._observers: Dict[Type[BaseEvent], List] = {}
    
    def registrar(self, tipo_evento: Type[BaseEvent], observer):
        """
        Registra um observer pra um tipo de evento
        
        Args:
            tipo_evento: Classe do evento (ex: EstoqueBaixoEvent)
            observer: Instância do observer
        """
        if tipo_evento not in self._observers:
            self._observers[tipo_evento] = []
        
        # Adiciona se ainda não tá na lista
        if observer not in self._observers[tipo_evento]:
            self._observers[tipo_evento].append(observer)
            print(f"✅ Observer {observer.__class__.__name__} "
                  f"registrado para {tipo_evento.__name__}")
    
    def remover(self, tipo_evento: Type[BaseEvent], observer):
        """
        Remove um observer
        
        Args:
            tipo_evento: Classe do evento
            observer: Instância do observer
        """
        if tipo_evento in self._observers:
            if observer in self._observers[tipo_evento]:
                self._observers[tipo_evento].remove(observer)
                print(f"❌ Observer {observer.__class__.__name__} removido")
    
    def notificar(self, evento: BaseEvent):
        """
        Notifica TODOS os observers registrados pro tipo do evento
        
        Args:
            evento: Instância do evento que aconteceu
        """
        tipo_evento = type(evento)
        
        # Busca observers registrados
        observers = self._observers.get(tipo_evento, [])
        
        if not observers:
            print(f"⚠️ Nenhum observer registrado para {tipo_evento.__name__}")
            return
        
        # Notifica cada observer
        print(f"📢 Notificando {len(observers)} observer(s) "
              f"sobre {tipo_evento.__name__}")
        
        for observer in observers:
            try:
                observer.notificar(evento)
            except Exception as e:
                # Se 1 observer falhar, não para os outros!
                print(f"❌ Erro ao notificar {observer.__class__.__name__}: {e}")
    
    def limpar(self):
        """Limpa todos os observers (útil pra testes)"""
        self._observers.clear()
        print("🧹 Todos os observers removidos")
    
    def listar_observers(self) -> Dict[str, List[str]]:
        """Lista todos os observers registrados (debug)"""
        resultado = {}
        for tipo_evento, observers in self._observers.items():
            resultado[tipo_evento.__name__] = [
                obs.__class__.__name__ for obs in observers
            ]
        return resultado


# Instância global (Singleton)
event_dispatcher = EventDispatcher()
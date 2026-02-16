"""
Eventos relacionados a estoque
Observer Pattern - Events concretos
"""

from typing import Dict, Any
from .base_event import BaseEvent


class EstoqueBaixoEvent(BaseEvent):
    """
    Evento disparado quando estoque fica abaixo do mínimo
    
    Observers podem:
    - Enviar email pro gerente
    - Salvar log
    - Enviar SMS
    - Criar tarefa no sistema
    """
    
    def __init__(
        self,
        medicamento_id: int,
        nome_medicamento: str,
        estoque_atual: int,
        estoque_minimo: int
    ):
        super().__init__()
        self.medicamento_id = medicamento_id
        self.nome_medicamento = nome_medicamento
        self.estoque_atual = estoque_atual
        self.estoque_minimo = estoque_minimo
    
    def _dados_especificos(self) -> Dict[str, Any]:
        return {
            "medicamento_id": self.medicamento_id,
            "nome_medicamento": self.nome_medicamento,
            "estoque_atual": self.estoque_atual,
            "estoque_minimo": self.estoque_minimo,
            "diferenca": self.estoque_minimo - self.estoque_atual
        }


class ProdutoVencendoEvent(BaseEvent):
    """
    Evento disparado quando produto está perto de vencer
    
    Observers podem:
    - Enviar alerta pro gerente
    - Marcar pra promoção
    - Avisar vendedores
    """
    
    def __init__(
        self,
        medicamento_id: int,
        nome_medicamento: str,
        lote_id: int,
        numero_lote: str,
        data_validade: str,
        dias_ate_vencer: int,
        quantidade: int
    ):
        super().__init__()
        self.medicamento_id = medicamento_id
        self.nome_medicamento = nome_medicamento
        self.lote_id = lote_id
        self.numero_lote = numero_lote
        self.data_validade = data_validade
        self.dias_ate_vencer = dias_ate_vencer
        self.quantidade = quantidade
    
    def _dados_especificos(self) -> Dict[str, Any]:
        return {
            "medicamento_id": self.medicamento_id,
            "nome_medicamento": self.nome_medicamento,
            "lote_id": self.lote_id,
            "numero_lote": self.numero_lote,
            "data_validade": self.data_validade,
            "dias_ate_vencer": self.dias_ate_vencer,
            "quantidade": self.quantidade,
            "urgencia": "CRITICO" if self.dias_ate_vencer <= 7 else "ATENCAO"
        }


class EstoqueAtualizadoEvent(BaseEvent):
    """
    Evento disparado quando estoque é atualizado
    
    Genérico pra qualquer alteração de estoque
    """
    
    def __init__(
        self,
        medicamento_id: int,
        nome_medicamento: str,
        quantidade_anterior: int,
        quantidade_nova: int,
        operacao: str  # "ENTRADA" ou "SAIDA"
    ):
        super().__init__()
        self.medicamento_id = medicamento_id
        self.nome_medicamento = nome_medicamento
        self.quantidade_anterior = quantidade_anterior
        self.quantidade_nova = quantidade_nova
        self.operacao = operacao
    
    def _dados_especificos(self) -> Dict[str, Any]:
        return {
            "medicamento_id": self.medicamento_id,
            "nome_medicamento": self.nome_medicamento,
            "quantidade_anterior": self.quantidade_anterior,
            "quantidade_nova": self.quantidade_nova,
            "operacao": self.operacao,
            "variacao": self.quantidade_nova - self.quantidade_anterior
        }
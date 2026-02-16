"""
Schemas Pydantic - Estoque
Define estrutura de dados para operações de estoque
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class AdicionarEstoqueRequest(BaseModel):
    """
    Schema para adicionar estoque
    
    Usado quando recebe produtos do fornecedor
    """
    quantidade: int = Field(
        ...,
        gt=0,  # Maior que zero
        description="Quantidade a adicionar no estoque"
    )
    numero_lote: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Número do lote recebido"
    )
    data_fabricacao: str = Field(
        ...,
        pattern=r'^\d{4}-\d{2}-\d{2}$',
        description="Data de fabricação no formato YYYY-MM-DD"
    )
    data_validade: str = Field(
        ...,
        pattern=r'^\d{4}-\d{2}-\d{2}$',
        description="Data de validade no formato YYYY-MM-DD"
    )
    fornecedor: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Nome do fornecedor"
    )
    
    class Config:
        """Configurações do schema"""
        json_schema_extra = {
            "example": {
                "quantidade": 200,
                "numero_lote": "LOTE-2024-001",
                "data_fabricacao": "2024-01-15",
                "data_validade": "2026-01-15",
                "fornecedor": "Farmacêutica ABC Ltda"
            }
        }


class RemoverEstoqueRequest(BaseModel):
    """
    Schema para remover estoque
    
    Usado quando vende ou dá baixa em produtos
    """
    quantidade: int = Field(
        ...,
        gt=0,  # Maior que zero
        description="Quantidade a remover do estoque"
    )
    motivo: Literal["VENDA", "VALIDADE", "PERDA", "DEVOLUCAO", "OUTRO"] = Field(
        ...,
        description="Motivo da remoção do estoque"
    )
    observacao: Optional[str] = Field(
        None,
        max_length=500,
        description="Observação adicional sobre a remoção"
    )
    
    class Config:
        """Configurações do schema"""
        json_schema_extra = {
            "example": {
                "quantidade": 10,
                "motivo": "VENDA",
                "observacao": "Venda para cliente João Silva"
            }
        }


class EstoqueResponse(BaseModel):
    """
    Schema para resposta de operações de estoque
    
    Retorna informações atualizadas do estoque
    """
    medicamento_id: int
    medicamento_nome: str
    estoque_atual: int
    estoque_minimo: int
    status: str  # "OK", "ATENCAO", "CRITICO"
    mensagem: Optional[str] = None
    
    class Config:
        """Configurações do schema"""
        from_attributes = True


class EstoqueBaixoItem(BaseModel):
    """
    Schema para item na lista de estoque baixo
    
    Representa um medicamento com estoque crítico
    """
    medicamento_id: int
    nome: str
    principio_ativo: str
    estoque_atual: int
    estoque_minimo: int
    diferenca: int  # Quanto falta pra ficar OK
    status: str  # "ATENCAO" ou "CRITICO"
    
    class Config:
        """Configurações do schema"""
        from_attributes = True
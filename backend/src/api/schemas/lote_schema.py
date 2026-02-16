"""
Schemas Pydantic - Lote
Define estrutura de dados da API
"""

from typing import Optional
from datetime import date

from pydantic import BaseModel, Field


class LoteCreate(BaseModel):
    """
    Schema para criar lote
    
    Valida os dados que vêm do cliente!
    """
    numero_lote: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Número do lote"
    )
    medicamento_id: int = Field(
        ...,
        gt=0,  # Maior que zero
        description="ID do medicamento"
    )
    quantidade: int = Field(
        ...,
        gt=0,
        description="Quantidade no lote"
    )
    data_fabricacao: date = Field(
        ...,
        description="Data de fabricação"
    )
    data_validade: date = Field(
        ...,
        description="Data de validade"
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
                "numero_lote": "LOTE-2024-001",
                "medicamento_id": 1,
                "quantidade": 500,
                "data_fabricacao": "2024-01-15",
                "data_validade": "2026-01-15",
                "fornecedor": "Farmacêutica ABC"
            }
        }


class LoteResponse(BaseModel):
    """
    Schema para resposta de lote
    
    Define como o lote é retornado pro cliente!
    """
    id: int
    numero_lote: str
    medicamento_id: int
    quantidade: int
    data_fabricacao: date
    data_validade: date
    fornecedor: str
    
    class Config:
        """Permite converter de ORM models"""
        from_attributes = True


class LoteUpdate(BaseModel):
    """
    Schema para atualizar lote
    
    Todos os campos são opcionais!
    """
    numero_lote: Optional[str] = Field(None, min_length=3, max_length=100)
    quantidade: Optional[int] = Field(None, gt=0)
    data_fabricacao: Optional[date] = None
    data_validade: Optional[date] = None
    fornecedor: Optional[str] = Field(None, min_length=3, max_length=200)
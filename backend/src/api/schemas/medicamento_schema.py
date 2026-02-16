"""
Schemas Pydantic - Medicamento
Define estrutura de dados da API
"""

from typing import Optional
from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, Field, field_validator


class MedicamentoCreate(BaseModel):
    """
    Schema para criar medicamento
    
    Valida os dados que vêm do cliente!
    """
    nome: str = Field(
        ...,  # Obrigatório
        min_length=3,
        max_length=200,
        description="Nome do medicamento"
    )
    principio_ativo: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Princípio ativo do medicamento"
    )
    preco: Decimal = Field(
        ...,
        gt=0,  # Maior que zero
        description="Preço do medicamento"
    )
    estoque_minimo: int = Field(
        ...,
        gt=0,  # Maior que zero
        description="Quantidade mínima em estoque"
    )
    requer_receita: bool = Field(  # ← NOVO! (Aula 10)
        False,  # Padrão: não controlado
        description="Se o medicamento requer receita médica (controlado)"
    )
    
    @field_validator('preco', mode='before')
    @classmethod
    def converter_preco(cls, v):
        """Converte string para Decimal se necessário"""
        if isinstance(v, str):
            try:
                return Decimal(v)
            except (InvalidOperation, ValueError):
                raise ValueError(f"Preço inválido: '{v}'. Use formato numérico (ex: 10.50)")
        return v
    
    class Config:
        """Configurações do schema"""
        json_schema_extra = {
            "example": {
                "nome": "Dipirona 500mg",
                "principio_ativo": "Dipirona Sódica",
                "preco": "8.50",
                "estoque_minimo": 100,
                "requer_receita": False  # ← NOVO! (Aula 10)
            }
        }


class MedicamentoResponse(BaseModel):
    """
    Schema para resposta de medicamento
    
    Define como o medicamento é retornado pro cliente!
    """
    id: int
    nome: str
    principio_ativo: str
    preco: Decimal
    estoque_minimo: int
    requer_receita: bool  # ← NOVO! (Aula 10)
    
    @field_validator('preco', mode='before')
    @classmethod
    def converter_preco_response(cls, v):
        """Converte string para Decimal se vier do banco"""
        if isinstance(v, str):
            return Decimal(v)
        return v
    
    class Config:
        """
        from_attributes = True permite converter de ORM models
        (antigamente era orm_mode = True)
        """
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: str(v)  # Serializa Decimal como string no JSON
        }


class MedicamentoUpdate(BaseModel):
    """
    Schema para atualizar medicamento
    
    Todos os campos são opcionais!
    """
    nome: Optional[str] = Field(None, min_length=3, max_length=200)
    principio_ativo: Optional[str] = Field(None, min_length=3, max_length=200)
    preco: Optional[Decimal] = Field(None, gt=0)
    estoque_minimo: Optional[int] = Field(None, gt=0)
    requer_receita: Optional[bool] = None  # ← NOVO! (Aula 10)
    
    @field_validator('preco', mode='before')
    @classmethod
    def converter_preco_update(cls, v):
        """Converte string para Decimal se necessário"""
        if v is not None and isinstance(v, str):
            try:
                return Decimal(v)
            except (InvalidOperation, ValueError):
                raise ValueError(f"Preço inválido: '{v}'. Use formato numérico (ex: 10.50)")
        return v
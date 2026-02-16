"""
Schemas Pydantic - Medicamento
Define estrutura de dados da API
"""

from typing import Optional
from decimal import Decimal, InvalidOperation
from datetime import date 
from typing import Dict, Any  

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
    
class CadastrarMedicamentoComLoteRequest(BaseModel):
    """Schema para cadastrar medicamento com lote inicial"""
    # Dados do medicamento
    nome: str = Field(..., min_length=3, max_length=200)
    principio_ativo: str = Field(..., min_length=3, max_length=200)
    preco: str = Field(..., pattern=r'^\d+(\.\d{2})?$', description="Preço no formato decimal (ex: 10.50)")
    requer_receita: bool = False  # Compatível com Aula 10!
    estoque_minimo: Optional[int] = Field(None, gt=0, description="Estoque mínimo (padrão: 50)")
    
    # Dados do lote inicial
    numero_lote: str = Field(..., min_length=3, max_length=100)
    quantidade_inicial: int = Field(..., gt=0, description="Quantidade inicial do lote")
    data_fabricacao: date
    data_validade: date
    fornecedor: str = Field(..., min_length=3, max_length=200)
    
    @validator("data_validade")
    def validar_validade_posterior(cls, v, values):
        """Valida que data de validade é posterior à fabricação"""
        if 'data_fabricacao' in values and v <= values['data_fabricacao']:
            raise ValueError("Data de validade deve ser posterior à data de fabricação")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Dipirona 500mg",
                "principio_ativo": "Dipirona Sódica",
                "preco": "8.50",
                "requer_receita": False,
                "estoque_minimo": 100,
                "numero_lote": "LOTE-2026-001",
                "quantidade_inicial": 500,
                "data_fabricacao": "2026-01-15",
                "data_validade": "2028-01-15",
                "fornecedor": "Farmacêutica ABC"
            }
        }


class CadastrarMedicamentoComLoteResponse(BaseModel):
    """Schema de resposta do cadastro com lote"""
    medicamento: Dict[str, Any]
    lote: Dict[str, Any]
    mensagem: str
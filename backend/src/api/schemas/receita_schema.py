"""
Schemas Pydantic - Receita Médica
Define estrutura de dados para validação de receitas
"""

from typing import Optional
from pydantic import BaseModel, Field


class ReceitaValidarRequest(BaseModel):
    """
    Schema para validar receita médica
    
    Usado para verificar se uma receita é válida
    """
    medicamento_id: int = Field(
        ...,
        gt=0,
        description="ID do medicamento a ser vendido"
    )
    
    # Dados do Paciente
    paciente_nome: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Nome completo do paciente"
    )
    paciente_cpf: str = Field(
        ...,
        pattern=r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
        description="CPF do paciente (com ou sem formatação)"
    )
    
    # Dados da Prescrição
    medicamento_nome: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Nome do medicamento prescrito"
    )
    quantidade: int = Field(
        ...,
        gt=0,
        description="Quantidade prescrita"
    )
    dosagem: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Dosagem prescrita (ex: '500mg', '2x ao dia')"
    )
    
    # Dados do Médico
    medico_nome: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Nome completo do médico"
    )
    medico_cpf: str = Field(
        ...,
        pattern=r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$',
        description="CPF do médico (com ou sem formatação)"
    )
    medico_crm: str = Field(
        ...,
        pattern=r'^\d{4,7}/[A-Z]{2}$',
        description="CRM do médico no formato 123456/UF"
    )
    
    # Datas
    data_emissao: str = Field(
        ...,
        pattern=r'^\d{4}-\d{2}-\d{2}$',
        description="Data de emissão da receita (YYYY-MM-DD)"
    )
    dias_validade: int = Field(
        30,
        ge=1,
        le=365,
        description="Validade da receita em dias (padrão: 30)"
    )
    
    class Config:
        """Configurações do schema"""
        json_schema_extra = {
            "example": {
                "medicamento_id": 1,
                "paciente_nome": "João da Silva",
                "paciente_cpf": "123.456.789-09",
                "medicamento_nome": "Rivotril 2mg",
                "quantidade": 30,
                "dosagem": "1 comprimido 2x ao dia",
                "medico_nome": "Dr. Carlos Souza",
                "medico_cpf": "987.654.321-00",
                "medico_crm": "123456/SP",
                "data_emissao": "2026-02-01",
                "dias_validade": 30
            }
        }


class ReceitaValidarResponse(BaseModel):
    """
    Schema para resposta da validação de receita
    """
    valido: bool
    medicamento_id: int
    medicamento_nome: str
    requer_receita: bool
    mensagem: str
    pode_vender: bool
    receita: Optional[dict] = None
    motivo: Optional[str] = None
    
    class Config:
        """Configurações do schema"""
        from_attributes = True
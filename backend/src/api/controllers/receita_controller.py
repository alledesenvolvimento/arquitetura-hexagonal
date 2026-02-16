"""
Controller - Receitas Médicas
Endpoints REST para validar receitas médicas
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from ..schemas.receita_schema import (
    ReceitaValidarRequest,
    ReceitaValidarResponse
)
from ...application.use_cases import ValidarReceitaUseCase
from ...adapters.repositories import MedicamentoRepositoryPostgres
from ...infrastructure.database import get_session


# Criar router do FastAPI
router = APIRouter(
    prefix="/receitas",
    tags=["Receitas Médicas"]
)


@router.post(
    "/validar",
    response_model=ReceitaValidarResponse,
    status_code=status.HTTP_200_OK,
    summary="Validar receita médica",
    description="Valida se uma receita médica é válida para compra de medicamento controlado"
)
def validar_receita(
    dados: ReceitaValidarRequest,
    session: Session = Depends(get_session)
):
    """
    Valida uma receita médica
    
    Use quando:
    - Cliente quer comprar medicamento controlado
    - Precisa validar receita antes da venda
    - Verificar se receita está válida
    
    Parâmetros:
    - **medicamento_id**: ID do medicamento a vender
    - **paciente_nome**: Nome completo do paciente
    - **paciente_cpf**: CPF do paciente
    - **medicamento_nome**: Nome do medicamento na receita
    - **quantidade**: Quantidade prescrita
    - **dosagem**: Dosagem (ex: "500mg 3x ao dia")
    - **medico_nome**: Nome do médico
    - **medico_cpf**: CPF do médico
    - **medico_crm**: CRM do médico (formato: 123456/UF)
    - **data_emissao**: Data da receita (YYYY-MM-DD)
    - **dias_validade**: Validade em dias (padrão: 30)
    
    Retorna:
    - **valido**: Se a receita é válida
    - **pode_vender**: Se pode prosseguir com a venda
    - **mensagem**: Feedback sobre a validação
    - **motivo**: Se rejeitada, o motivo
    """
    try:
        # 1. Criar repositório
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        
        # 2. Criar use case
        use_case = ValidarReceitaUseCase(medicamento_repo)
        
        # 3. Executar
        resultado = use_case.execute(
            medicamento_id=dados.medicamento_id,
            paciente_nome=dados.paciente_nome,
            paciente_cpf=dados.paciente_cpf,
            medicamento_nome=dados.medicamento_nome,
            quantidade=dados.quantidade,
            dosagem=dados.dosagem,
            medico_nome=dados.medico_nome,
            medico_cpf=dados.medico_cpf,
            medico_crm=dados.medico_crm,
            data_emissao=dados.data_emissao,
            dias_validade=dados.dias_validade
        )
        
        # 4. Retornar
        return ReceitaValidarResponse(**resultado)
        
    except ValueError as e:
        # Erro de validação
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Erro inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao validar receita: {str(e)}"
        )
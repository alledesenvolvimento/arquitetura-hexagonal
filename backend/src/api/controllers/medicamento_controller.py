"""
Controller - Medicamentos
Endpoints REST para gerenciar medicamentos
"""

from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from ..schemas.medicamento_schema import (
    MedicamentoCreate,
    MedicamentoResponse,
    MedicamentoUpdate
)
from ...application.use_cases import (
    CadastrarMedicamentoUseCase,
    ListarMedicamentosUseCase
)
from ...adapters.repositories import MedicamentoRepositoryPostgres
from ...infrastructure.database import get_session


# Criar router do FastAPI
router = APIRouter(
    prefix="/medicamentos",
    tags=["Medicamentos"]
)


@router.post(
    "/",
    response_model=MedicamentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo medicamento",
    description="Cria um novo medicamento no sistema"
)
def criar_medicamento(
    medicamento_data: MedicamentoCreate,
    session: Session = Depends(get_session)
):
    """
    Cadastra um novo medicamento no sistema
    
    O Pydantic valida automaticamente os dados de entrada.
    Se inválidos, retorna erro 422 automaticamente.
    
    - **nome**: Nome do medicamento (min 3 caracteres)
    - **principio_ativo**: Princípio ativo do medicamento
    - **preco**: Preço no formato decimal (ex: 10.50)
    - **estoque_minimo**: Quantidade mínima em estoque (> 0)
    """
    try:
        # 1. Criar repositório
        repository = MedicamentoRepositoryPostgres(session)
        
        # 2. Criar use case
        use_case = CadastrarMedicamentoUseCase(repository)
        
        # 3. Executar
        medicamento = use_case.execute(medicamento_data.dict())
        
        # 4. Retornar
        return medicamento
        
    except ValueError as e:
        # Erro de validação de domínio
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Erro inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cadastrar medicamento: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[MedicamentoResponse],
    summary="Listar medicamentos",
    description="Retorna lista de todos os medicamentos cadastrados"
)
def listar_medicamentos(session: Session = Depends(get_session)):
    """
    Lista todos os medicamentos cadastrados
    
    Retorna:
    - Array vazio [] se não houver medicamentos
    - Array com medicamentos se houver cadastros
    """
    try:
        # 1. Criar repositório
        repository = MedicamentoRepositoryPostgres(session)
        
        # 2. Criar use case
        use_case = ListarMedicamentosUseCase(repository)
        
        # 3. Executar e retornar
        medicamentos = use_case.execute()
        
        return medicamentos
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar medicamentos: {str(e)}"
        )


@router.get(
    "/{medicamento_id}",
    response_model=MedicamentoResponse,
    summary="Buscar medicamento por ID",
    description="Retorna um medicamento específico pelo ID"
)
def buscar_medicamento(
    medicamento_id: int,
    session: Session = Depends(get_session)
):
    """
    Busca um medicamento específico pelo ID
    
    Args:
    - **medicamento_id**: ID do medicamento (número inteiro)
    
    Retorna:
    - Medicamento encontrado (200)
    - Erro 404 se medicamento não existe
    """
    try:
        repository = MedicamentoRepositoryPostgres(session)
        medicamento = repository.buscar_por_id(medicamento_id)
        
        if medicamento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento {medicamento_id} não encontrado"
            )
        
        return medicamento
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar medicamento: {str(e)}"
        )


@router.delete(
    "/{medicamento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar medicamento",
    description="Remove um medicamento do sistema"
)
def deletar_medicamento(
    medicamento_id: int,
    session: Session = Depends(get_session)
):
    """
    Remove um medicamento do sistema
    
    Args:
    - **medicamento_id**: ID do medicamento a deletar
    
    Retorna:
    - 204 (No Content) se deletado com sucesso
    - 404 se medicamento não existe
    
    ATENÇÃO: Esta ação é irreversível!
    """
    try:
        repository = MedicamentoRepositoryPostgres(session)
        deletado = repository.deletar(medicamento_id)
        
        if not deletado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento {medicamento_id} não encontrado"
            )
        
        # 204 não retorna conteúdo
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar medicamento: {str(e)}"
        )
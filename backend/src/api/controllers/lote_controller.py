"""
Controller - Lotes
Endpoints REST para gerenciar lotes
"""

from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from ..schemas.lote_schema import (
    LoteCreate,
    LoteResponse,
    LoteUpdate
)
from ...adapters.repositories import LoteRepositoryPostgres
from ...infrastructure.database import get_session
from ...domain.entities import Lote


# Criar router
router = APIRouter(
    prefix="/lotes",
    tags=["Lotes"]
)


@router.post(
    "/",
    response_model=LoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo lote",
    description="Registra um novo lote de medicamentos"
)
def criar_lote(
    lote_data: LoteCreate,
    session: Session = Depends(get_session)
):
    """
    Registra um novo lote de medicamentos no sistema
    
    IMPORTANTE: O medicamento_id deve existir previamente!
    
    - **numero_lote**: Identificação única do lote (ex: LOTE-2024-001)
    - **medicamento_id**: ID do medicamento (deve estar cadastrado!)
    - **quantidade**: Quantidade de unidades no lote
    - **data_fabricacao**: Data de fabricação
    - **data_validade**: Data de validade
    - **fornecedor**: Nome do fornecedor
    """
    try:
        repository = LoteRepositoryPostgres(session)
        
        # Converter Pydantic → Entidade
        lote = Lote(**lote_data.dict())
        
        # Salvar
        lote_salvo = repository.salvar(lote)
        
        return lote_salvo
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cadastrar lote: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[LoteResponse],
    summary="Listar lotes",
    description="Retorna lista de todos os lotes cadastrados"
)
def listar_lotes(session: Session = Depends(get_session)):
    """
    Lista todos os lotes
    
    Retorna array vazio se não houver lotes cadastrados.
    """
    try:
        repository = LoteRepositoryPostgres(session)
        lotes = repository.listar_todos()
        
        return lotes
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar lotes: {str(e)}"
        )


@router.get(
    "/{lote_id}",
    response_model=LoteResponse,
    summary="Buscar lote por ID",
    description="Retorna um lote específico pelo ID"
)
def buscar_lote(
    lote_id: int,
    session: Session = Depends(get_session)
):
    """
    Busca lote por ID
    
    - **lote_id**: ID do lote
    
    Retorna erro 404 se não encontrado.
    """
    try:
        repository = LoteRepositoryPostgres(session)
        lote = repository.buscar_por_id(lote_id)
        
        if lote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lote {lote_id} não encontrado"
            )
        
        return lote
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar lote: {str(e)}"
        )


@router.get(
    "/medicamento/{medicamento_id}",
    response_model=List[LoteResponse],
    summary="Listar lotes por medicamento",
    description="Retorna todos os lotes de um medicamento específico"
)
def listar_lotes_por_medicamento(
    medicamento_id: int,
    session: Session = Depends(get_session)
):
    """
    Lista todos os lotes de um medicamento específico
    
    Args:
    - **medicamento_id**: ID do medicamento
    
    Útil para:
    - Verificar estoque disponível de um medicamento
    - Ver todos os lotes (vencidos ou não)
    - Planejar reposição de estoque
    """
    try:
        repository = LoteRepositoryPostgres(session)
        lotes = repository.buscar_por_medicamento(medicamento_id)
        
        return lotes
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar lotes: {str(e)}"
        )


@router.delete(
    "/{lote_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar lote",
    description="Remove um lote do sistema"
)
def deletar_lote(
    lote_id: int,
    session: Session = Depends(get_session)
):
    """
    Deleta lote por ID
    
    - **lote_id**: ID do lote a deletar
    
    Retorna 204 (No Content) se deletado com sucesso.
    Retorna 404 se lote não existe.
    """
    try:
        repository = LoteRepositoryPostgres(session)
        deletado = repository.deletar(lote_id)
        
        if not deletado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lote {lote_id} não encontrado"
            )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar lote: {str(e)}"
        )
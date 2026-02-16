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
from ..schemas.estoque_schema import (
    AdicionarEstoqueRequest,
    RemoverEstoqueRequest,
    EstoqueResponse,
    EstoqueBaixoItem
)
from ...application.use_cases import (
    CadastrarMedicamentoUseCase,
    ListarMedicamentosUseCase,
    AdicionarEstoqueUseCase,
    RemoverEstoqueUseCase,
    VerificarEstoqueBaixoUseCase
)
from ...adapters.repositories import (
    MedicamentoRepositoryPostgres,
    LoteRepositoryPostgres
)
from ...infrastructure.database import get_session


# Criar router do FastAPI
router = APIRouter(
    prefix="/medicamentos",
    tags=["Medicamentos"]
)


# ==========================================
# ENDPOINTS DE MEDICAMENTOS (CRUD)
# ==========================================

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


# ==========================================
# ENDPOINTS DE GESTÃO DE ESTOQUE
# ==========================================

@router.post(
    "/{medicamento_id}/estoque/adicionar",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
    summary="Adicionar estoque",
    description="Adiciona produtos ao estoque (entrada de mercadorias)"
)
def adicionar_estoque(
    medicamento_id: int,
    dados: AdicionarEstoqueRequest,
    session: Session = Depends(get_session)
):
    """
    Adiciona quantidade ao estoque de um medicamento
    
    Use quando:
    - Receber produtos do fornecedor
    - Entrada de mercadorias
    - Reposição de estoque
    
    Parâmetros:
    - **medicamento_id**: ID do medicamento
    - **quantidade**: Quantidade a adicionar (> 0)
    - **numero_lote**: Número do lote recebido
    - **data_fabricacao**: Data de fabricação (YYYY-MM-DD)
    - **data_validade**: Data de validade (YYYY-MM-DD)
    - **fornecedor**: Nome do fornecedor
    """
    try:
        # 1. Criar repositórios
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        
        # 2. Criar use case
        use_case = AdicionarEstoqueUseCase(medicamento_repo, lote_repo)
        
        # 3. Executar
        resultado = use_case.execute(
            medicamento_id=medicamento_id,
            quantidade=dados.quantidade,
            numero_lote=dados.numero_lote,
            data_fabricacao=dados.data_fabricacao,
            data_validade=dados.data_validade,
            fornecedor=dados.fornecedor
        )
        
        # 4. Retornar
        return EstoqueResponse(
            medicamento_id=resultado["medicamento_id"],
            medicamento_nome=resultado["medicamento_nome"],
            estoque_atual=resultado["estoque_atual"],
            estoque_minimo=resultado["estoque_minimo"],
            status=resultado["status"],
            mensagem=resultado["mensagem"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar estoque: {str(e)}"
        )


@router.post(
    "/{medicamento_id}/estoque/remover",
    response_model=EstoqueResponse,
    status_code=status.HTTP_200_OK,
    summary="Remover estoque",
    description="Remove produtos do estoque (saída/venda)"
)
def remover_estoque(
    medicamento_id: int,
    dados: RemoverEstoqueRequest,
    session: Session = Depends(get_session)
):
    """
    Remove quantidade do estoque de um medicamento
    
    Use quando:
    - Vender produtos
    - Dar baixa em produtos vencidos
    - Registrar perda/devolução
    
    Parâmetros:
    - **medicamento_id**: ID do medicamento
    - **quantidade**: Quantidade a remover (> 0)
    - **motivo**: Motivo da remoção (VENDA, VALIDADE, PERDA, etc)
    - **observacao**: Observação adicional (opcional)
    
    Regra importante:
    - Não pode remover mais do que tem em estoque!
    """
    try:
        # 1. Criar repositórios
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        
        # 2. Criar use case
        use_case = RemoverEstoqueUseCase(medicamento_repo, lote_repo)
        
        # 3. Executar
        resultado = use_case.execute(
            medicamento_id=medicamento_id,
            quantidade=dados.quantidade,
            motivo=dados.motivo,
            observacao=dados.observacao
        )
        
        # 4. Retornar
        return EstoqueResponse(
            medicamento_id=resultado["medicamento_id"],
            medicamento_nome=resultado["medicamento_nome"],
            estoque_atual=resultado["estoque_atual"],
            estoque_minimo=resultado["estoque_minimo"],
            status=resultado["status"],
            mensagem=resultado["mensagem"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover estoque: {str(e)}"
        )


@router.get(
    "/estoque-baixo",
    response_model=List[EstoqueBaixoItem],
    summary="Listar estoque baixo",
    description="Retorna medicamentos com estoque crítico ou abaixo do mínimo"
)
def listar_estoque_baixo(session: Session = Depends(get_session)):
    """
    Lista todos os medicamentos com estoque baixo
    
    Retorna:
    - Medicamentos com estoque zerado (CRÍTICO)
    - Medicamentos abaixo do estoque mínimo (ATENÇÃO)
    
    Ordenado por prioridade (críticos primeiro)
    """
    try:
        # 1. Criar repositórios
        medicamento_repo = MedicamentoRepositoryPostgres(session)
        lote_repo = LoteRepositoryPostgres(session)
        
        # 2. Criar use case
        use_case = VerificarEstoqueBaixoUseCase(medicamento_repo, lote_repo)
        
        # 3. Executar
        alertas = use_case.execute()
        
        # 4. Converter para schema
        return [
            EstoqueBaixoItem(**alerta)
            for alerta in alertas
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar estoque baixo: {str(e)}"
        )
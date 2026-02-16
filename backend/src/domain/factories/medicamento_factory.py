"""
Factory Pattern: Medicamento Factory
Cria medicamentos de forma padronizada com validações
"""

from decimal import Decimal
from typing import Optional

from src.domain.entities import Medicamento, Lote


class MedicamentoFactory:
    """
    Factory para criar medicamentos
    
    Responsabilidades:
    1. Validar dados de entrada
    2. Aplicar valores padrão
    3. Criar medicamento
    4. Opcionalmente criar lote inicial
    5. Garantir consistência
    """
    
    # Valores padrão da fábrica
    ESTOQUE_MINIMO_PADRAO = 50
    PRECO_MINIMO = Decimal("0.01")
    PRECO_MAXIMO = Decimal("10000.00")
    
    @classmethod
    def criar(
        cls,
        nome: str,
        principio_ativo: str,
        preco: float,
        estoque_minimo: Optional[int] = None,
        controlado: bool = False
    ) -> Medicamento:
        """
        Cria um medicamento com validações completas
        
        Args:
            nome: Nome do medicamento
            principio_ativo: Princípio ativo
            preco: Preço unitário
            estoque_minimo: Estoque mínimo (usa padrão se não informado)
            controlado: Se é medicamento controlado
            
        Returns:
            Medicamento criado e validado
            
        Raises:
            ValueError: Se dados inválidos
        """
        # 1. Validar dados de entrada
        cls._validar_nome(nome)
        cls._validar_principio_ativo(principio_ativo)
        
        # 2. Converter e validar preço
        preco_decimal = cls._converter_e_validar_preco(preco)
        
        # 3. Aplicar valores padrão
        if estoque_minimo is None:
            estoque_minimo = cls.ESTOQUE_MINIMO_PADRAO
        
        # 4. Validar estoque mínimo
        cls._validar_estoque_minimo(estoque_minimo)
        
        # 5. Criar medicamento
        medicamento = Medicamento(
            nome=nome.strip().title(),  # Padroniza nome
            principio_ativo=principio_ativo.strip().title(),
            preco=preco_decimal,
            estoque_minimo=estoque_minimo,
            requer_receita=controlado  # ← Usa requer_receita!
        )
        
        return medicamento
    
    @classmethod
    def criar_com_lote_inicial(
        cls,
        nome: str,
        principio_ativo: str,
        preco: float,
        numero_lote: str,
        quantidade_inicial: int,
        data_fabricacao: str,
        data_validade: str,
        fornecedor: str,
        estoque_minimo: Optional[int] = None,
        controlado: bool = False
    ) -> tuple[Medicamento, Lote]:
        """
        Cria medicamento JÁ COM lote inicial
        
        Útil quando está cadastrando produto novo que já chegou!
        
        Args:
            [medicamento args...]
            numero_lote: Número do lote
            quantidade_inicial: Quantidade no lote
            data_fabricacao: Data de fabricação (YYYY-MM-DD)
            data_validade: Data de validade (YYYY-MM-DD)
            fornecedor: Nome do fornecedor
            
        Returns:
            Tupla (medicamento, lote)
        """
        from datetime import date
        
        # 1. Criar medicamento
        medicamento = cls.criar(
            nome=nome,
            principio_ativo=principio_ativo,
            preco=preco,
            estoque_minimo=estoque_minimo,
            controlado=controlado
        )
        
        # 2. Validar quantidade inicial
        if quantidade_inicial <= 0:
            raise ValueError("Quantidade inicial deve ser maior que zero")
        
        # 3. Converter datas
        try:
            data_fab = date.fromisoformat(data_fabricacao)
            data_val = date.fromisoformat(data_validade)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Formato de data inválido: {e}")
        
        # 4. Criar lote
        lote = Lote(
            numero_lote=numero_lote.strip().upper(),  # Padroniza
            medicamento_id=medicamento.id,
            quantidade=quantidade_inicial,
            data_fabricacao=data_fab,
            data_validade=data_val,
            fornecedor=fornecedor.strip().title()  # Padroniza
        )
        
        return medicamento, lote
    
    @staticmethod
    def _validar_nome(nome: str) -> None:
        """Valida nome do medicamento"""
        if not nome or not nome.strip():
            raise ValueError("Nome do medicamento é obrigatório")
        
        if len(nome.strip()) < 3:
            raise ValueError("Nome deve ter no mínimo 3 caracteres")
        
        if len(nome.strip()) > 200:
            raise ValueError("Nome deve ter no máximo 200 caracteres")
    
    @staticmethod
    def _validar_principio_ativo(principio: str) -> None:
        """Valida princípio ativo"""
        if not principio or not principio.strip():
            raise ValueError("Princípio ativo é obrigatório")
        
        if len(principio.strip()) < 3:
            raise ValueError("Princípio ativo deve ter no mínimo 3 caracteres")
    
    @classmethod
    def _converter_e_validar_preco(cls, preco: float) -> Decimal:
        """Converte e valida preço"""
        try:
            preco_decimal = Decimal(str(preco))
        except (ValueError, TypeError):
            raise ValueError("Preço inválido")
        
        if preco_decimal < cls.PRECO_MINIMO:
            raise ValueError(
                f"Preço deve ser no mínimo {cls.PRECO_MINIMO}"
            )
        
        if preco_decimal > cls.PRECO_MAXIMO:
            raise ValueError(
                f"Preço deve ser no máximo {cls.PRECO_MAXIMO}"
            )
        
        return preco_decimal
    
    @staticmethod
    def _validar_estoque_minimo(estoque_minimo: int) -> None:
        """Valida estoque mínimo"""
        if estoque_minimo < 0:
            raise ValueError("Estoque mínimo não pode ser negativo")
        
        if estoque_minimo > 10000:
            raise ValueError("Estoque mínimo muito alto (máx: 10.000)")
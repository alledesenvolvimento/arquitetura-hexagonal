"""
Entidade de Domínio: Medicamento
Representa um medicamento no sistema AlleFarma

Esta é uma entidade PURA - não depende de nada externo!
"""

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional


@dataclass
class Medicamento:
    """
    Entidade que representa um medicamento na farmácia
    
    Atributos:
        id: Identificador único (opcional, gerado pelo banco)
        nome: Nome do medicamento
        principio_ativo: Princípio ativo (substância que age no organismo)
        preco: Preço unitário
        estoque_minimo: Quantidade mínima antes de alertar
        descricao: Descrição detalhada (opcional)
        estoque_atual: Quantidade em estoque (opcional, padrão 0)
        requer_receita: Se precisa de receita médica (opcional, padrão False)
        data_validade: Data de validade do lote atual (opcional)
    """
    
    nome: str
    principio_ativo: str
    preco: Decimal
    estoque_minimo: int
    descricao: Optional[str] = None
    estoque_atual: int = 0
    requer_receita: bool = False
    data_validade: Optional[date] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """
        Validações executadas após criar o objeto
        Aqui ficam as REGRAS DE NEGÓCIO!
        """
        self._validar_nome()
        self._validar_principio_ativo()
        self._validar_preco()
        self._validar_estoque()
        if self.data_validade:
            self._validar_validade()
    
    def _validar_nome(self):
        """Regra: Nome é obrigatório e não pode ser vazio"""
        if not self.nome or self.nome.strip() == "":
            raise ValueError("Nome do medicamento é obrigatório!")
        
        if len(self.nome) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres!")
    
    def _validar_principio_ativo(self):
        """Regra: Princípio ativo é obrigatório"""
        if not self.principio_ativo or self.principio_ativo.strip() == "":
            raise ValueError("Princípio ativo é obrigatório!")
        
        if len(self.principio_ativo) < 3:
            raise ValueError("Princípio ativo deve ter pelo menos 3 caracteres!")
    
    def _validar_preco(self):
        """Regra: Preço deve ser positivo"""
        if self.preco <= 0:
            raise ValueError("Preço deve ser maior que zero!")
    
    def _validar_estoque(self):
        """Regra: Estoques devem ser não-negativos"""
        if self.estoque_atual < 0:
            raise ValueError("Estoque atual não pode ser negativo!")
        
        if self.estoque_minimo < 0:
            raise ValueError("Estoque mínimo não pode ser negativo!")
    
    def _validar_validade(self):
        """Regra: Data de validade deve ser futura"""
        if self.data_validade <= date.today():
            raise ValueError("Medicamento com validade vencida ou no dia de hoje não pode ser cadastrado!")
    
    # ============ MÉTODOS DE NEGÓCIO ============
    
    def esta_vencido(self) -> bool:
        """Verifica se o medicamento está vencido"""
        if not self.data_validade:
            return False
        return date.today() > self.data_validade
    
    def estoque_baixo(self) -> bool:
        """Verifica se o estoque está abaixo do mínimo"""
        return self.estoque_atual < self.estoque_minimo
    
    def pode_vender(self, quantidade: int) -> bool:
        """
        Verifica se pode vender determinada quantidade
        
        Regras:
        - Não pode estar vencido
        - Precisa ter estoque suficiente
        """
        if self.esta_vencido():
            raise ValueError(f"Medicamento {self.nome} está vencido!")
        
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero!")
        
        if self.estoque_atual < quantidade:
            raise ValueError(
                f"Estoque insuficiente! Disponível: {self.estoque_atual}, "
                f"Solicitado: {quantidade}"
            )
        
        return True
    
    def baixar_estoque(self, quantidade: int):
        """
        Reduz o estoque após uma venda
        """
        if self.pode_vender(quantidade):
            self.estoque_atual -= quantidade
    
    def repor_estoque(self, quantidade: int):
        """
        Aumenta o estoque após recebimento
        """
        if quantidade <= 0:
            raise ValueError("Quantidade de reposição deve ser maior que zero!")
        
        self.estoque_atual += quantidade
    
    # ============ VALIDAÇÕES DE MEDICAMENTO CONTROLADO (AULA 10) ============
    
    def requer_receita_medica(self) -> bool:
        """
        Verifica se este medicamento requer receita médica
        
        Returns:
            True se é controlado, False se é venda livre
        """
        return self.requer_receita
    
    def validar_venda_controlada(self, receita=None):
        """
        Valida se pode vender medicamento controlado
        
        Args:
            receita: Receita médica (obrigatória se controlado)
            
        Raises:
            ValueError: Se controlado sem receita ou receita inválida
        """
        if not self.requer_receita:
            # Medicamento comum, pode vender sem receita
            return True
        
        # Medicamento controlado!
        if receita is None:
            raise ValueError(
                f"Medicamento controlado '{self.nome}' requer receita médica! "
                "Não é possível vender sem apresentar receita válida."
            )
        
        # Verifica se receita está válida
        if not receita.esta_valida():
            dias = receita.dias_restantes()
            raise ValueError(
                f"Receita vencida há {abs(dias)} dias! "
                f"Data de vencimento: {receita.data_vencimento()}"
            )
        
        # Verifica se o medicamento na receita bate
        if receita.medicamento_nome.lower() not in self.nome.lower():
            raise ValueError(
                f"Receita é para '{receita.medicamento_nome}', "
                f"mas está tentando comprar '{self.nome}'"
            )
        
        return True
    
    def __str__(self):
        """Representação amigável do medicamento"""
        return f"{self.nome} ({self.principio_ativo}) - R$ {self.preco:.2f} (Estoque: {self.estoque_atual})"
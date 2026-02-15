"""
Entidade de Domínio: Lote
Representa um lote de medicamentos no sistema AlleFarma

Um lote agrupa medicamentos fabricados juntos, com mesma validade
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class Lote:
    """
    Entidade que representa um lote de medicamentos
    
    Atributos:
        id: Identificador único (opcional, gerado pelo banco)
        numero_lote: Código de identificação do lote
        medicamento_id: ID do medicamento deste lote
        quantidade: Quantidade de unidades neste lote
        data_fabricacao: Quando foi fabricado
        data_validade: Até quando pode ser vendido
        fornecedor: Nome do fornecedor/fabricante
    """
    
    numero_lote: str
    medicamento_id: int
    quantidade: int
    data_fabricacao: date
    data_validade: date
    fornecedor: str
    id: Optional[int] = None
    
    def __post_init__(self):
        """
        Validações executadas após criar o objeto
        Aqui ficam as REGRAS DE NEGÓCIO!
        """
        self._validar_numero_lote()
        self._validar_quantidade()
        self._validar_datas()
        self._validar_fornecedor()
    
    def _validar_numero_lote(self):
        """Regra: Número do lote é obrigatório"""
        if not self.numero_lote or self.numero_lote.strip() == "":
            raise ValueError("Número do lote é obrigatório!")
        
        if len(self.numero_lote) < 3:
            raise ValueError("Número do lote deve ter pelo menos 3 caracteres!")
    
    def _validar_quantidade(self):
        """Regra: Quantidade deve ser positiva"""
        if self.quantidade <= 0:
            raise ValueError("Quantidade do lote deve ser maior que zero!")
    
    def _validar_datas(self):
        """Regra: Datas devem fazer sentido"""
        # Data de fabricação não pode ser futura
        if self.data_fabricacao > date.today():
            raise ValueError("Data de fabricação não pode ser no futuro!")
        
        # Data de validade deve ser após fabricação
        if self.data_validade <= self.data_fabricacao:
            raise ValueError(
                "Data de validade deve ser posterior à data de fabricação!"
            )
        
        # Aviso se já estiver vencido
        if self.data_validade <= date.today():
            raise ValueError("Lote com validade vencida não pode ser cadastrado!")
    
    def _validar_fornecedor(self):
        """Regra: Fornecedor é obrigatório"""
        if not self.fornecedor or self.fornecedor.strip() == "":
            raise ValueError("Fornecedor é obrigatório!")
        
        if len(self.fornecedor) < 3:
            raise ValueError("Nome do fornecedor deve ter pelo menos 3 caracteres!")
    
    # ============ MÉTODOS DE NEGÓCIO ============
    
    def esta_vencido(self) -> bool:
        """Verifica se o lote está vencido"""
        return date.today() > self.data_validade
    
    def dias_para_vencer(self) -> int:
        """
        Calcula quantos dias faltam para vencer
        Retorna negativo se já estiver vencido
        """
        delta = self.data_validade - date.today()
        return delta.days
    
    def vence_em_breve(self, dias: int = 30) -> bool:
        """
        Verifica se o lote vence em breve
        Por padrão, considera "breve" como 30 dias
        """
        if self.esta_vencido():
            return False  # Já venceu, não "vence em breve"
        
        return self.dias_para_vencer() <= dias
    
    def pode_ser_comercializado(self) -> bool:
        """
        Verifica se o lote pode ser comercializado
        
        Regras:
        - Não pode estar vencido
        - Precisa ter quantidade disponível
        """
        if self.esta_vencido():
            raise ValueError(
                f"Lote {self.numero_lote} está vencido! "
                f"Venceu em {self.data_validade.strftime('%d/%m/%Y')}"
            )
        
        if self.quantidade <= 0:
            raise ValueError(
                f"Lote {self.numero_lote} não tem quantidade disponível!"
            )
        
        return True
    
    def retirar_quantidade(self, quantidade: int):
        """
        Retira uma quantidade do lote (após uma venda)
        """
        if quantidade <= 0:
            raise ValueError("Quantidade a retirar deve ser maior que zero!")
        
        if quantidade > self.quantidade:
            raise ValueError(
                f"Quantidade insuficiente no lote! "
                f"Disponível: {self.quantidade}, Solicitado: {quantidade}"
            )
        
        self.quantidade -= quantidade
    
    def adicionar_quantidade(self, quantidade: int):
        """
        Adiciona quantidade ao lote (devolução, ajuste de estoque)
        """
        if quantidade <= 0:
            raise ValueError("Quantidade a adicionar deve ser maior que zero!")
        
        self.quantidade += quantidade
    
    def __str__(self):
        """Representação amigável do lote"""
        status = "VENCIDO" if self.esta_vencido() else "VÁLIDO"
        return (
            f"Lote {self.numero_lote} - {status} "
            f"(Qtd: {self.quantidade}, Val: {self.data_validade.strftime('%d/%m/%Y')})"
        )
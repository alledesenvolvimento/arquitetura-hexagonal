"""
Value Object: Receita Médica
Representa uma receita médica válida
"""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
from .cpf import CPF


@dataclass(frozen=True)
class Receita:
    """
    Value Object que representa uma receita médica
    
    Receita é imutável e valida todos os dados necessários
    para venda de medicamentos controlados
    """
    
    # Dados do Paciente
    paciente_nome: str
    paciente_cpf: CPF
    
    # Dados da Prescrição
    medicamento_nome: str
    quantidade: int
    dosagem: str
    
    # Dados do Médico
    medico_nome: str
    medico_cpf: CPF
    medico_crm: str  # Formato: "123456/SP"
    
    # Datas
    data_emissao: date
    dias_validade: int = 30  # Padrão: 30 dias (tarja vermelha)
    
    def __post_init__(self):
        """Valida receita após criação"""
        self._validar_paciente()
        self._validar_prescricao()
        self._validar_medico()
        self._validar_datas()
    
    def _validar_paciente(self):
        """Valida dados do paciente"""
        if not self.paciente_nome or len(self.paciente_nome.strip()) < 3:
            raise ValueError("Nome do paciente deve ter pelo menos 3 caracteres")
        
        # CPF já é validado pelo Value Object CPF
    
    def _validar_prescricao(self):
        """Valida dados da prescrição"""
        if not self.medicamento_nome or len(self.medicamento_nome.strip()) < 3:
            raise ValueError("Nome do medicamento deve ter pelo menos 3 caracteres")
        
        if self.quantidade <= 0:
            raise ValueError("Quantidade prescrita deve ser maior que zero")
        
        if not self.dosagem or len(self.dosagem.strip()) < 2:
            raise ValueError("Dosagem é obrigatória (ex: '500mg', '2x ao dia')")
    
    def _validar_medico(self):
        """Valida dados do médico"""
        if not self.medico_nome or len(self.medico_nome.strip()) < 3:
            raise ValueError("Nome do médico deve ter pelo menos 3 caracteres")
        
        # CPF já é validado pelo Value Object CPF
        
        # Valida formato do CRM (número/UF)
        import re
        if not re.match(r'^\d{4,7}/[A-Z]{2}$', self.medico_crm):
            raise ValueError(
                f"CRM inválido: {self.medico_crm}. "
                "Formato esperado: 123456/UF (ex: 123456/SP)"
            )
    
    def _validar_datas(self):
        """Valida datas da receita"""
        # Data de emissão não pode ser futura
        if self.data_emissao > date.today():
            raise ValueError(
                f"Data de emissão não pode ser futura: {self.data_emissao}"
            )
        
        # Dias de validade deve ser positivo e razoável
        if self.dias_validade <= 0 or self.dias_validade > 365:
            raise ValueError(
                f"Dias de validade inválido: {self.dias_validade}. "
                "Deve ser entre 1 e 365 dias"
            )
    
    def esta_valida(self) -> bool:
        """
        Verifica se a receita ainda está válida
        
        Returns:
            True se válida, False se vencida
        """
        data_vencimento = self.data_emissao + timedelta(days=self.dias_validade)
        return date.today() <= data_vencimento
    
    def dias_restantes(self) -> int:
        """
        Retorna quantos dias faltam para vencer
        
        Returns:
            Número de dias (negativo se já venceu)
        """
        data_vencimento = self.data_emissao + timedelta(days=self.dias_validade)
        return (data_vencimento - date.today()).days
    
    def data_vencimento(self) -> date:
        """Retorna a data de vencimento da receita"""
        return self.data_emissao + timedelta(days=self.dias_validade)
    
    def __str__(self) -> str:
        """Representação amigável"""
        status = "VÁLIDA" if self.esta_valida() else "VENCIDA"
        return (
            f"Receita {status} - "
            f"{self.medicamento_nome} para {self.paciente_nome} "
            f"(Dr. {self.medico_nome} CRM {self.medico_crm})"
        )
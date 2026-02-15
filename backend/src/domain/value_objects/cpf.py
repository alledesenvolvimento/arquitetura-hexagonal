"""
Value Object: CPF
Representa um CPF válido no sistema AlleFarma

Este é um Value Object IMUTÁVEL - não pode ser alterado após criação!
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)  # ← IMUTÁVEL!
class CPF:
    """
    Value Object que representa um CPF
    
    Características:
    - Imutável (frozen=True)
    - Valida formato e dígitos verificadores
    - Formata automaticamente
    """
    
    numero: str
    
    def __post_init__(self):
        """
        Validação executada após criar o objeto
        Como é frozen, usamos object.__setattr__ para definir valores
        """
        # Remove formatação (pontos, traços)
        apenas_numeros = re.sub(r'[^0-9]', '', self.numero)
        
        # Valida
        self._validar_cpf(apenas_numeros)
        
        # Armazena formatado
        # Como é frozen, usamos object.__setattr__
        object.__setattr__(self, 'numero', self._formatar_cpf(apenas_numeros))
    
    def _validar_cpf(self, cpf: str):
        """
        Valida CPF (formato e dígitos verificadores)
        """
        # Deve ter 11 dígitos
        if len(cpf) != 11:
            raise ValueError("CPF deve ter 11 dígitos!")
        
        # Não pode ser todos iguais (000.000.000-00, 111.111.111-11, etc)
        if cpf == cpf[0] * 11:
            raise ValueError("CPF inválido!")
        
        # Valida dígitos verificadores
        if not self._validar_digitos_verificadores(cpf):
            raise ValueError("CPF com dígitos verificadores inválidos!")
    
    def _validar_digitos_verificadores(self, cpf: str) -> bool:
        """
        Valida os dois dígitos verificadores do CPF
        """
        # Primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = 11 - (soma % 11)
        digito1 = 0 if digito1 > 9 else digito1
        
        if int(cpf[9]) != digito1:
            return False
        
        # Segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = 11 - (soma % 11)
        digito2 = 0 if digito2 > 9 else digito2
        
        return int(cpf[10]) == digito2
    
    def _formatar_cpf(self, cpf: str) -> str:
        """
        Formata CPF no padrão XXX.XXX.XXX-XX
        """
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    def sem_formatacao(self) -> str:
        """
        Retorna CPF sem formatação (só números)
        """
        return re.sub(r'[^0-9]', '', self.numero)
    
    def __str__(self):
        """Representação amigável"""
        return self.numero
"""
Value Object: Telefone
Representa um número de telefone válido no sistema AlleFarma

Este é um Value Object IMUTÁVEL - não pode ser alterado após criação!
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)  # ← IMUTÁVEL!
class Telefone:
    """
    Value Object que representa um Telefone
    
    Características:
    - Imutável (frozen=True)
    - Valida DDD e formato
    - Suporta fixo (8 dígitos) e celular (9 dígitos)
    - Formata automaticamente
    """
    
    numero: str
    
    def __post_init__(self):
        """
        Validação executada após criar o objeto
        """
        # Remove formatação
        apenas_numeros = re.sub(r'[^0-9]', '', self.numero)
        
        # Valida
        self._validar_telefone(apenas_numeros)
        
        # Armazena formatado
        object.__setattr__(self, 'numero', self._formatar_telefone(apenas_numeros))
    
    def _validar_telefone(self, telefone: str):
        """
        Valida número de telefone
        Formato: DDD (2 dígitos) + Número (8 ou 9 dígitos)
        """
        # Deve ter 10 dígitos (fixo) ou 11 dígitos (celular)
        if len(telefone) not in [10, 11]:
            raise ValueError(
                "Telefone deve ter 10 dígitos (fixo) ou 11 dígitos (celular)!"
            )
        
        # DDD deve estar entre 11 e 99
        ddd = int(telefone[:2])
        if ddd < 11 or ddd > 99:
            raise ValueError(f"DDD inválido: {ddd}")
        
        # Se for celular (11 dígitos), deve começar com 9
        if len(telefone) == 11 and telefone[2] != '9':
            raise ValueError("Celular deve começar com 9 após o DDD!")
    
    def _formatar_telefone(self, telefone: str) -> str:
        """
        Formata telefone no padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
        """
        ddd = telefone[:2]
        
        if len(telefone) == 11:  # Celular
            return f"({ddd}) {telefone[2:7]}-{telefone[7:]}"
        else:  # Fixo
            return f"({ddd}) {telefone[2:6]}-{telefone[6:]}"
    
    def sem_formatacao(self) -> str:
        """
        Retorna telefone sem formatação (só números)
        """
        return re.sub(r'[^0-9]', '', self.numero)
    
    def ddd(self) -> str:
        """Retorna apenas o DDD"""
        apenas_numeros = self.sem_formatacao()
        return apenas_numeros[:2]
    
    def eh_celular(self) -> bool:
        """Verifica se é celular (11 dígitos)"""
        return len(self.sem_formatacao()) == 11
    
    def __str__(self):
        """Representação amigável"""
        return self.numero
"""
Value Objects do AlleFarma
Objetos imutáveis que representam valores do domínio
"""

from .cpf import CPF
from .telefone import Telefone
from .receita import Receita

__all__ = ['CPF', 'Telefone', 'Receita']
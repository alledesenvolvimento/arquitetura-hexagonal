"""
Modelos SQLAlchemy (Tabelas do Banco)
Representam as tabelas no PostgreSQL
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base


class LoteModel(Base):
    """
    Modelo (Tabela) de Lote no banco de dados
    
    Esta classe vira uma TABELA no PostgreSQL!
    """
    __tablename__ = "lotes"
    
    # Colunas
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_lote = Column(String(100), nullable=False, unique=True)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_fabricacao = Column(Date, nullable=False)
    data_validade = Column(Date, nullable=False)
    fornecedor = Column(String(200), nullable=False)
    
    def __repr__(self):
        return f"<LoteModel(id={self.id}, numero_lote='{self.numero_lote}')>"


class MedicamentoModel(Base):
    """
    Modelo (Tabela) de Medicamento no banco de dados
    """
    __tablename__ = "medicamentos"
    
    # Colunas
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    principio_ativo = Column(String(200), nullable=False)
    preco = Column(String(20), nullable=False)  # Decimal vira String
    estoque_minimo = Column(Integer, nullable=False)
    descricao = Column(String(500), nullable=True)
    estoque_atual = Column(Integer, default=0)
    requer_receita = Column(Integer, default=0)  # 0=False, 1=True (SQLite style)
    data_validade = Column(Date, nullable=True)
    
    def __repr__(self):
        return f"<MedicamentoModel(id={self.id}, nome='{self.nome}')>"
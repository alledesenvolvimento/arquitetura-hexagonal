"""
Script para criar tabelas no banco
Roda uma única vez pra criar a estrutura
"""

from .base import engine, Base
from .models import LoteModel, MedicamentoModel


def create_tables():
    """Cria todas as tabelas no banco"""
    print("🗄️  Criando tabelas no PostgreSQL...")
    
    # Isso cria todas as tabelas definidas nos modelos
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tabelas criadas com sucesso!")
    print("   - medicamentos")
    print("   - lotes")


if __name__ == "__main__":
    create_tables()
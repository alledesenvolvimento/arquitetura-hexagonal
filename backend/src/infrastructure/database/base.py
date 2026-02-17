"""
Configuração do Banco de Dados
Usa variáveis de ambiente do arquivo .env
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# ======================================================
# URL DO BANCO — vem do .env, nunca hardcoded no código!
# ======================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Valor padrão caso .env não exista (evita crashes)
    "postgresql://postgres:postgres@localhost:5432/allefarma"
)

# Criar engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False  # True para ver SQL no terminal (útil pra debug)
)

# Criar fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para os modelos ORM
Base = declarative_base()


def get_session():
    """
    Dependency Injection do FastAPI

    Cria uma sessão, passa pro endpoint, fecha no final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
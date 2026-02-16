"""
Base do SQLAlchemy
Configuração central do ORM
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Base para os modelos
Base = declarative_base()

# Configuração do banco
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/allefarma"

# Engine (motor de conexão)
engine = create_engine(DATABASE_URL, echo=True)

# Session (sessão pra interagir com o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Retorna uma sessão do banco"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
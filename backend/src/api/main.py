"""
AlleFarma - Sistema de Gestão Farmacêutica
Aula 1: Primeira API simples
"""

from fastapi import FastAPI

# Criar instância do FastAPI
app = FastAPI(
    title="AlleFarma API",
    description="Sistema de Gestão Farmacêutica com Arquitetura Hexagonal",
    version="0.1.0"
)


# Rota raiz - apenas pra testar
@app.get("/")
def home():
    """
    Rota de boas-vindas
    """
    return {
        "mensagem": "Bem-vindo ao AlleFarma! 💊",
        "versao": "0.1.0",
        "status": "online"
    }


# Rota de teste pra ver se tá funcionando
@app.get("/health")
def health_check():
    """
    Verifica se a API tá rodando
    """
    return {
        "status": "healthy",
        "servico": "AlleFarma API"
    }


# Rota de teste com medicamentos (dados fake, só pra ver funcionando)
@app.get("/medicamentos")
def listar_medicamentos():
    """
    Lista alguns medicamentos de exemplo
    Nas próximas aulas vamos fazer isso de verdade!
    """
    return {
        "medicamentos": [
            {
                "id": 1,
                "nome": "Dipirona 500mg",
                "preco": 8.50,
                "estoque": 100
            },
            {
                "id": 2,
                "nome": "Paracetamol 750mg",
                "preco": 12.00,
                "estoque": 50
            }
        ],
        "total": 2
    }
"""
API Principal do AlleFarma
FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controllers import medicamento_controller, lote_controller, receita_controller
from src.api.controllers.relatorio_controller import router as relatorio_router


# Criar aplicação FastAPI
app = FastAPI(
    title="AlleFarma API",
    description="API REST para gestão farmacêutica usando Arquitetura Hexagonal",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)


# Configurar CORS (permitir frontend acessar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE...
    allow_headers=["*"],
)


# Registrar routers (controllers)
app.include_router(medicamento_controller.router)
app.include_router(lote_controller.router)
app.include_router(receita_controller.router)
app.include_router(relatorio_router)


@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raiz
    
    Retorna informações básicas da API
    """
    return {
        "message": "AlleFarma API - Arquitetura Hexagonal",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check
    
    Verifica se a API está funcionando
    """
    return {
        "status": "healthy",
        "service": "AlleFarma API"
    }
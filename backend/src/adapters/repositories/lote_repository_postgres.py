"""
Adapter: Repositório de Lotes no PostgreSQL
Implementa LoteRepositoryPort salvando no banco real

Agora os dados persistem! 🎉
"""

from typing import Optional, List
from datetime import date, timedelta
from sqlalchemy.orm import Session

from src.domain.entities import Lote
from src.domain.ports import LoteRepositoryPort
from src.infrastructure.database import LoteModel


class LoteRepositoryPostgres(LoteRepositoryPort):
    """
    Implementação PostgreSQL do repositório de lotes
    
    Salva lotes em tabelas reais do PostgreSQL!
    Dados persistem mesmo depois de reiniciar!
    """
    
    def __init__(self, session: Session):
        """
        Inicializa com sessão do banco
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self.session = session
    
    def _entidade_para_modelo(self, lote: Lote) -> LoteModel:
        """
        Converte Entidade → Modelo (Domain → Database)
        
        Args:
            lote: Entidade do domínio
            
        Returns:
            Modelo do SQLAlchemy
        """
        return LoteModel(
            id=lote.id,
            numero_lote=lote.numero_lote,
            medicamento_id=lote.medicamento_id,
            quantidade=lote.quantidade,
            data_fabricacao=lote.data_fabricacao,
            data_validade=lote.data_validade,
            fornecedor=lote.fornecedor
        )
    
    def _modelo_para_entidade(self, modelo: LoteModel) -> Lote:
        """
        Converte Modelo → Entidade (Database → Domain)
        
        Args:
            modelo: Modelo do SQLAlchemy
            
        Returns:
            Entidade do domínio
        """
        return Lote(
            id=modelo.id,
            numero_lote=modelo.numero_lote,
            medicamento_id=modelo.medicamento_id,
            quantidade=modelo.quantidade,
            data_fabricacao=modelo.data_fabricacao,
            data_validade=modelo.data_validade,
            fornecedor=modelo.fornecedor
        )
    
    def salvar(self, lote: Lote) -> Lote:
        """
        Salva lote no PostgreSQL
        
        Args:
            lote: Lote a ser salvo
            
        Returns:
            Lote salvo (com ID gerado pelo banco)
        """
        # Converte entidade → modelo
        lote_model = self._entidade_para_modelo(lote)
        
        # Salva no banco
        self.session.add(lote_model)
        self.session.commit()
        self.session.refresh(lote_model)  # Pega ID gerado
        
        # Converte modelo → entidade
        return self._modelo_para_entidade(lote_model)
    
    def buscar_por_id(self, id: int) -> Optional[Lote]:
        """
        Busca lote por ID no PostgreSQL
        
        Args:
            id: ID do lote
            
        Returns:
            Lote encontrado ou None
        """
        lote_model = self.session.query(LoteModel).filter(
            LoteModel.id == id
        ).first()
        
        if lote_model is None:
            return None
        
        return self._modelo_para_entidade(lote_model)
    
    def listar_todos(self) -> List[Lote]:
        """
        Lista todos os lotes do PostgreSQL
        
        Returns:
            Lista de todos os lotes
        """
        lotes_model = self.session.query(LoteModel).all()
        
        return [
            self._modelo_para_entidade(modelo)
            for modelo in lotes_model
        ]
    
    def buscar_por_medicamento(self, medicamento_id: int) -> List[Lote]:
        """
        Busca lotes de um medicamento no PostgreSQL
        
        Args:
            medicamento_id: ID do medicamento
            
        Returns:
            Lista de lotes do medicamento
        """
        lotes_model = self.session.query(LoteModel).filter(
            LoteModel.medicamento_id == medicamento_id
        ).all()
        
        return [
            self._modelo_para_entidade(modelo)
            for modelo in lotes_model
        ]
    
    def listar_vencendo_em(self, dias: int) -> List[Lote]:
        """
        Lista lotes que vencem nos próximos X dias (PostgreSQL)
        
        Args:
            dias: Número de dias
            
        Returns:
            Lista de lotes vencendo
        """
        data_limite = date.today() + timedelta(days=dias)
        
        lotes_model = self.session.query(LoteModel).filter(
            LoteModel.data_validade <= data_limite,
            LoteModel.data_validade >= date.today()
        ).all()
        
        return [
            self._modelo_para_entidade(modelo)
            for modelo in lotes_model
        ]
    
    def atualizar(self, lote: Lote) -> Lote:
        """
        Atualiza lote no PostgreSQL
        
        Args:
            lote: Lote com dados atualizados
            
        Returns:
            Lote atualizado
            
        Raises:
            ValueError: Se lote não existir
        """
        if lote.id is None:
            raise ValueError("Lote precisa ter ID para atualizar!")
        
        # Busca no banco
        lote_model = self.session.query(LoteModel).filter(
            LoteModel.id == lote.id
        ).first()
        
        if lote_model is None:
            raise ValueError(f"Lote {lote.id} não encontrado!")
        
        # Atualiza campos
        lote_model.numero_lote = lote.numero_lote
        lote_model.medicamento_id = lote.medicamento_id
        lote_model.quantidade = lote.quantidade
        lote_model.data_fabricacao = lote.data_fabricacao
        lote_model.data_validade = lote.data_validade
        lote_model.fornecedor = lote.fornecedor
        
        # Salva mudanças
        self.session.commit()
        self.session.refresh(lote_model)
        
        return self._modelo_para_entidade(lote_model)
    
    def deletar(self, id: int) -> bool:
        """
        Deleta lote do PostgreSQL
        
        Args:
            id: ID do lote
            
        Returns:
            True se deletou, False se não encontrou
        """
        lote_model = self.session.query(LoteModel).filter(
            LoteModel.id == id
        ).first()
        
        if lote_model is None:
            return False
        
        self.session.delete(lote_model)
        self.session.commit()
        
        return True
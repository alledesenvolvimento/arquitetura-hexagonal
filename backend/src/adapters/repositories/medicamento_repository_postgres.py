"""
Adapter: Repositório de Medicamentos no PostgreSQL
Implementa MedicamentoRepositoryPort salvando no banco real
"""

from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session

from src.domain.entities import Medicamento
from src.domain.ports import MedicamentoRepositoryPort
from src.infrastructure.database import MedicamentoModel


class MedicamentoRepositoryPostgres(MedicamentoRepositoryPort):
    """
    Implementação PostgreSQL do repositório de medicamentos
    
    Converte entre Entidade (domínio) ↔ Modelo (banco de dados)
    Salva dados de verdade no PostgreSQL!
    
    IMPORTANTE: MedicamentoModel foi criado na Aula 7!
    Se você não tem esse modelo, volte e crie antes de continuar.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa repositório
        
        Args:
            session: Sessão do SQLAlchemy para acessar o banco
        """
        self.session = session

    def _entidade_para_modelo(self, medicamento: Medicamento) -> MedicamentoModel:
        """
        Converte Entidade → Modelo
    
        Traduz objeto de domínio (Medicamento) para objeto do banco (MedicamentoModel)
    
        Args:
            medicamento: Entidade de domínio
        
        Returns:
            Modelo do SQLAlchemy pronto pra salvar no banco
        """
        return MedicamentoModel(
            id=medicamento.id,
            nome=medicamento.nome,
            principio_ativo=medicamento.principio_ativo,
            preco=str(medicamento.preco),
            estoque_minimo=medicamento.estoque_minimo,
            requer_receita=1 if medicamento.requer_receita else 0  # ← NOVO! (Aula 10) - Converte   bool → int
        )
    
    def _modelo_para_entidade(self, modelo: MedicamentoModel) -> Medicamento:
        """
        Converte Modelo → Entidade
    
        Traduz objeto do banco (MedicamentoModel) para objeto de domínio (Medicamento)
    
        Args:
            modelo: Modelo do SQLAlchemy
        
        Returns:
            Entidade de domínio limpa (sem dependências do banco)
        """
        from decimal import Decimal
    
        return Medicamento(
            id=modelo.id,
            nome=modelo.nome,
            principio_ativo=modelo.principio_ativo,
            preco=Decimal(modelo.preco) if isinstance(modelo.preco, str) else modelo.preco,
            estoque_minimo=modelo.estoque_minimo,
            requer_receita=bool(modelo.requer_receita)  #  - Converte int → bool
        )
    

    
    def salvar(self, medicamento: Medicamento) -> Medicamento:
        """
        Salva medicamento no PostgreSQL
        
        Se o medicamento não tem ID, gera um novo.
        Se já tem ID, atualiza o existente.
        
        Args:
            medicamento: Entidade a salvar
            
        Returns:
            Entidade salva (agora com ID gerado pelo banco)
        """
        # Converter Entidade → Modelo
        modelo = self._entidade_para_modelo(medicamento)
        
        # Salvar no banco
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        
        # Converter Modelo → Entidade
        return self._modelo_para_entidade(modelo)
    
    def buscar_por_id(self, id: int) -> Optional[Medicamento]:
        """
        Busca medicamento por ID no PostgreSQL
        
        Args:
            id: ID do medicamento a buscar
            
        Returns:
            Medicamento encontrado ou None se não existir
        """
        modelo = self.session.query(MedicamentoModel).filter(
            MedicamentoModel.id == id
        ).first()
        
        if modelo is None:
            return None
        
        return self._modelo_para_entidade(modelo)
    
    def listar_todos(self) -> List[Medicamento]:
        """
        Lista todos os medicamentos cadastrados no PostgreSQL
        
        Returns:
            Lista de medicamentos (pode ser vazia)
        """
        modelos = self.session.query(MedicamentoModel).all()
        
        return [
            self._modelo_para_entidade(modelo)
            for modelo in modelos
        ]
    
    def atualizar(self, medicamento: Medicamento) -> Medicamento:
        """
        Atualiza medicamento existente
        
        Args:
            medicamento: Entidade com dados atualizados
            
        Returns:
            Entidade atualizada
            
        Raises:
            ValueError: Se medicamento não tem ID ou não existe
        """
        if medicamento.id is None:
            raise ValueError("Medicamento precisa ter ID para atualizar!")
        
        # Buscar no banco
        modelo = self.session.query(MedicamentoModel).filter(
            MedicamentoModel.id == medicamento.id
        ).first()
        
        if modelo is None:
            raise ValueError(f"Medicamento {medicamento.id} não encontrado!")
        
        # Atualizar campos
        modelo.nome = medicamento.nome
        modelo.principio_ativo = medicamento.principio_ativo
        modelo.preco = str(medicamento.preco)
        modelo.estoque_minimo = medicamento.estoque_minimo
        
        # Salvar
        self.session.commit()
        self.session.refresh(modelo)
        
        return self._modelo_para_entidade(modelo)
    
    def deletar(self, id: int) -> bool:
        """
        Deleta medicamento do PostgreSQL
        
        Args:
            id: ID do medicamento a deletar
            
        Returns:
            True se deletado com sucesso, False se não existe
        """
        modelo = self.session.query(MedicamentoModel).filter(
            MedicamentoModel.id == id
        ).first()
        
        if modelo is None:
            return False
        
        self.session.delete(modelo)
        self.session.commit()
        
        return True
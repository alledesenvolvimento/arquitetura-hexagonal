"""
Adapter: Serviço de Estoque em Memória
Implementa o EstoqueServicePort usando estruturas em memória

ATENÇÃO: Dados são perdidos ao encerrar o programa!
"""

from typing import Dict, List
from src.domain.ports import EstoqueServicePort, MedicamentoRepositoryPort, LoteRepositoryPort


class EstoqueServiceMemory(EstoqueServicePort):
    """
    Implementação em memória do serviço de estoque
    
    Gerencia operações de estoque usando dados em memória
    """
    
    def __init__(
        self,
        medicamento_repository: MedicamentoRepositoryPort,
        lote_repository: LoteRepositoryPort
    ):
        """
        Inicializa o serviço com seus repositórios
        
        Args:
            medicamento_repository: Repositório de medicamentos
            lote_repository: Repositório de lotes
        """
        self.medicamento_repo = medicamento_repository
        self.lote_repo = lote_repository
        
        # Controle interno de movimentações (em memória)
        self._movimentacoes: List[Dict] = []
    
    def verificar_disponibilidade(self, medicamento_id: int, quantidade: int) -> bool:
        """
        Verifica se tem quantidade disponível de um medicamento
        
        Args:
            medicamento_id: ID do medicamento
            quantidade: Quantidade desejada
            
        Returns:
            True se tem disponível, False caso contrário
        """
        # Busca todos os lotes deste medicamento
        lotes = self.lote_repo.buscar_por_medicamento(medicamento_id)
        
        # Soma quantidade disponível (lotes não vencidos)
        quantidade_disponivel = sum(
            lote.quantidade
            for lote in lotes
            if not lote.esta_vencido()
        )
        
        return quantidade_disponivel >= quantidade
    
    def registrar_entrada(self, medicamento_id: int, lote_id: int, quantidade: int) -> None:
        """
        Registra entrada de estoque (compra/recebimento)
        
        Args:
            medicamento_id: ID do medicamento
            lote_id: ID do lote recebido
            quantidade: Quantidade recebida
            
        Raises:
            ValueError: Se dados inválidos
        """
        # Validações
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero!")
        
        # Busca o lote
        lote = self.lote_repo.buscar_por_id(lote_id)
        if lote is None:
            raise ValueError(f"Lote {lote_id} não encontrado!")
        
        if lote.medicamento_id != medicamento_id:
            raise ValueError(f"Lote {lote_id} não pertence ao medicamento {medicamento_id}!")
        
        # Adiciona quantidade ao lote
        lote.adicionar_quantidade(quantidade)
        self.lote_repo.atualizar(lote)
        
        # Registra movimentação
        self._movimentacoes.append({
            'tipo': 'ENTRADA',
            'medicamento_id': medicamento_id,
            'lote_id': lote_id,
            'quantidade': quantidade
        })
    
    def registrar_saida(self, medicamento_id: int, quantidade: int) -> None:
        """
        Registra saída de estoque (venda)
        Usa FIFO (First In, First Out) - lotes mais antigos primeiro
        
        Args:
            medicamento_id: ID do medicamento
            quantidade: Quantidade vendida
            
        Raises:
            ValueError: Se estoque insuficiente ou dados inválidos
        """
        # Validações
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero!")
        
        # Verifica disponibilidade
        if not self.verificar_disponibilidade(medicamento_id, quantidade):
            raise ValueError(f"Estoque insuficiente de medicamento {medicamento_id}!")
        
        # Busca lotes disponíveis (ordena por data de fabricação - FIFO)
        lotes = self.lote_repo.buscar_por_medicamento(medicamento_id)
        lotes_disponiveis = [
            lote for lote in lotes
            if not lote.esta_vencido() and lote.quantidade > 0
        ]
        lotes_disponiveis.sort(key=lambda l: l.data_fabricacao)
        
        # Retira quantidade dos lotes (FIFO)
        quantidade_restante = quantidade
        
        for lote in lotes_disponiveis:
            if quantidade_restante == 0:
                break
            
            # Quanto retirar deste lote?
            quantidade_retirar = min(quantidade_restante, lote.quantidade)
            
            # Retira do lote
            lote.retirar_quantidade(quantidade_retirar)
            self.lote_repo.atualizar(lote)
            
            # Registra movimentação
            self._movimentacoes.append({
                'tipo': 'SAIDA',
                'medicamento_id': medicamento_id,
                'lote_id': lote.id,
                'quantidade': quantidade_retirar
            })
            
            quantidade_restante -= quantidade_retirar
    
    def consultar_estoque_atual(self, medicamento_id: int) -> Dict[str, int]:
        """
        Retorna informações de estoque de um medicamento
        
        Args:
            medicamento_id: ID do medicamento
            
        Returns:
            Dicionário com informações de estoque
        """
        # Busca lotes
        lotes = self.lote_repo.buscar_por_medicamento(medicamento_id)
        
        # Calcula totais
        estoque_total = sum(lote.quantidade for lote in lotes)
        
        estoque_disponivel = sum(
            lote.quantidade
            for lote in lotes
            if not lote.esta_vencido()
        )
        
        estoque_vencido = sum(
            lote.quantidade
            for lote in lotes
            if lote.esta_vencido()
        )
        
        return {
            "estoque_total": estoque_total,
            "estoque_disponivel": estoque_disponivel,
            "estoque_vencido": estoque_vencido,
            "quantidade_lotes": len(lotes)
        }
    
    def listar_estoque_baixo(self) -> List[Dict]:
        """
        Lista medicamentos com estoque abaixo do mínimo
        
        Returns:
            Lista de dicionários com informações dos medicamentos
        """
        medicamentos = self.medicamento_repo.listar_todos()
        estoque_baixo = []
        
        for medicamento in medicamentos:
            # Consulta estoque
            estoque = self.consultar_estoque_atual(medicamento.id)
            
            # Verifica se está abaixo do mínimo
            if estoque['estoque_disponivel'] < medicamento.estoque_minimo:
                estoque_baixo.append({
                    'medicamento_id': medicamento.id,
                    'nome': medicamento.nome,
                    'estoque_atual': estoque['estoque_disponivel'],
                    'estoque_minimo': medicamento.estoque_minimo,
                    'diferenca': medicamento.estoque_minimo - estoque['estoque_disponivel']
                })
        
        return estoque_baixo
"""
Use Case: Validar Receita Médica
Valida se uma receita médica é válida e pode ser usada
"""

from typing import Dict, Any
from datetime import date

from src.domain.value_objects import CPF, Receita
from src.domain.ports import MedicamentoRepositoryPort


class ValidarReceitaUseCase:
    """
    Use Case para validar receita médica
    
    Fluxo:
    1. Cria Value Object Receita (valida formato)
    2. Verifica se receita está válida (não vencida)
    3. Busca medicamento no sistema
    4. Verifica se medicamento requer receita
    5. Valida se receita serve para este medicamento
    6. Retorna resultado da validação
    
    Regras de Negócio:
    - Receita deve ter todos os dados obrigatórios
    - CPFs devem ser válidos
    - CRM deve estar no formato correto
    - Receita não pode estar vencida
    - Medicamento na receita deve bater com o solicitado
    """
    
    def __init__(self, medicamento_repository: MedicamentoRepositoryPort):
        """
        Inicializa o use case
        
        Args:
            medicamento_repository: Repositório de medicamentos
        """
        self.medicamento_repo = medicamento_repository
    
    def execute(
        self,
        medicamento_id: int,
        paciente_nome: str,
        paciente_cpf: str,
        medicamento_nome: str,
        quantidade: int,
        dosagem: str,
        medico_nome: str,
        medico_cpf: str,
        medico_crm: str,
        data_emissao: str,
        dias_validade: int = 30
    ) -> Dict[str, Any]:
        """
        Executa a validação da receita
        
        Args:
            medicamento_id: ID do medicamento a comprar
            paciente_nome: Nome do paciente
            paciente_cpf: CPF do paciente
            medicamento_nome: Nome do medicamento na receita
            quantidade: Quantidade prescrita
            dosagem: Dosagem prescrita
            medico_nome: Nome do médico
            medico_cpf: CPF do médico
            medico_crm: CRM do médico (formato: 123456/UF)
            data_emissao: Data de emissão (YYYY-MM-DD)
            dias_validade: Validade em dias (padrão 30)
            
        Returns:
            Dicionário com resultado da validação
            
        Raises:
            ValueError: Se dados inválidos ou receita rejeitada
        """
        # 1. Buscar medicamento
        medicamento = self.medicamento_repo.buscar_por_id(medicamento_id)
        if not medicamento:
            raise ValueError(f"Medicamento {medicamento_id} não encontrado!")
        
        # 2. Se não é controlado, não precisa de receita
        if not medicamento.requer_receita:
            return {
                "valido": True,
                "medicamento_id": medicamento.id,
                "medicamento_nome": medicamento.nome,
                "requer_receita": False,
                "mensagem": "Medicamento de venda livre - receita não necessária",
                "pode_vender": True
            }
        
        # 3. É controlado! Validar receita
        try:
            # Criar Value Objects CPF
            cpf_paciente = CPF(paciente_cpf)
            cpf_medico = CPF(medico_cpf)
            
            # Converter data
            from datetime import datetime
            data_emissao_date = datetime.strptime(data_emissao, "%Y-%m-%d").date()
            
            # Criar Value Object Receita
            receita = Receita(
                paciente_nome=paciente_nome,
                paciente_cpf=cpf_paciente,
                medicamento_nome=medicamento_nome,
                quantidade=quantidade,
                dosagem=dosagem,
                medico_nome=medico_nome,
                medico_cpf=cpf_medico,
                medico_crm=medico_crm,
                data_emissao=data_emissao_date,
                dias_validade=dias_validade
            )
            
        except ValueError as e:
            # Erro na criação dos Value Objects
            raise ValueError(f"Dados da receita inválidos: {str(e)}")
        
        # 4. Validar receita contra medicamento
        try:
            medicamento.validar_venda_controlada(receita)
        except ValueError as e:
            # Receita não serve para este medicamento
            return {
                "valido": False,
                "medicamento_id": medicamento.id,
                "medicamento_nome": medicamento.nome,
                "requer_receita": True,
                "motivo": str(e),
                "pode_vender": False
            }
        
        # 5. Tudo válido!
        return {
            "valido": True,
            "medicamento_id": medicamento.id,
            "medicamento_nome": medicamento.nome,
            "requer_receita": True,
            "receita": {
                "paciente": paciente_nome,
                "medico": f"Dr. {medico_nome} (CRM {medico_crm})",
                "valida_ate": receita.data_vencimento().isoformat(),
                "dias_restantes": receita.dias_restantes()
            },
            "mensagem": "Receita válida! Venda autorizada.",
            "pode_vender": True
        }
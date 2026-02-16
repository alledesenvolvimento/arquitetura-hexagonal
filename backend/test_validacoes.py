"""
Testes de Validações Complexas
Testando CPF, Receita e validações compostas
"""

from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import text

from src.domain.value_objects import CPF, Receita
from src.domain.entities import Medicamento
from src.adapters.repositories import MedicamentoRepositoryPostgres
from src.application.use_cases import (
    CadastrarMedicamentoUseCase,
    ValidarReceitaUseCase
)
from src.infrastructure.database import SessionLocal


def limpar_banco():
    """Limpa dados de teste"""
    session = SessionLocal()
    try:
        session.execute(text("DELETE FROM lotes"))
        session.execute(text("DELETE FROM medicamentos"))
        session.commit()
        print("🧹 Banco limpo!\n")
    finally:
        session.close()


def teste_cpf_valido():
    """Testa criação de CPF válido"""
    print("🧪 Teste 1: CPF Válido")
    print("-" * 50)
    
    # CPF válido com formatação
    cpf1 = CPF("123.456.789-09")
    print(f"✅ CPF criado: {cpf1}")
    
    # CPF válido sem formatação
    cpf2 = CPF("12345678909")
    print(f"✅ CPF criado: {cpf2}")
    
    # Comparação por valor
    print(f"   São iguais? {cpf1 == cpf2}")
    
    print()


def teste_cpf_invalido():
    """Testa validação de CPF inválido"""
    print("🧪 Teste 2: CPF Inválido")
    print("-" * 50)
    
    # CPF com dígitos errados
    try:
        CPF("123.456.789-00")  # Dígitos incorretos
        print("❌ ERRO: Deveria ter rejeitado CPF inválido!")
    except ValueError as e:
        print(f"✅ CPF rejeitado: {e}")
    
    # CPF com sequência repetida
    try:
        CPF("111.111.111-11")
        print("❌ ERRO: Deveria ter rejeitado sequência!")
    except ValueError as e:
        print(f"✅ Sequência rejeitada: {e}")
    
    print()


def teste_receita_valida():
    """Testa criação de receita válida"""
    print("🧪 Teste 3: Receita Válida")
    print("-" * 50)
    
    cpf_paciente = CPF("123.456.789-09")
    cpf_medico = CPF("987.654.321-00")
    
    receita = Receita(
        paciente_nome="João da Silva",
        paciente_cpf=cpf_paciente,
        medicamento_nome="Rivotril 2mg",
        quantidade=30,
        dosagem="1 comprimido 2x ao dia",
        medico_nome="Dr. Carlos Souza",
        medico_cpf=cpf_medico,
        medico_crm="123456/SP",
        data_emissao=date.today(),
        dias_validade=30
    )
    
    print(f"✅ Receita criada: {receita}")
    print(f"   Válida? {receita.esta_valida()}")
    print(f"   Vence em: {receita.dias_restantes()} dias")
    print(f"   Data vencimento: {receita.data_vencimento()}")
    
    print()


def teste_receita_vencida():
    """Testa detecção de receita vencida"""
    print("🧪 Teste 4: Receita Vencida")
    print("-" * 50)
    
    cpf_paciente = CPF("123.456.789-09")
    cpf_medico = CPF("987.654.321-00")
    
    # Receita emitida há 31 dias (vencida!)
    receita = Receita(
        paciente_nome="Maria Santos",
        paciente_cpf=cpf_paciente,
        medicamento_nome="Antibiótico",
        quantidade=10,
        dosagem="500mg 3x ao dia",
        medico_nome="Dr. Ana Costa",
        medico_cpf=cpf_medico,
        medico_crm="654321/RJ",
        data_emissao=date.today() - timedelta(days=31),
        dias_validade=30
    )
    
    print(f"📋 Receita: {receita}")
    print(f"   Válida? {receita.esta_valida()}")
    print(f"   Venceu há: {abs(receita.dias_restantes())} dias")
    
    print()


def teste_validar_medicamento_controlado():
    """Testa validação de venda de medicamento controlado"""
    print("🧪 Teste 5: Medicamento Controlado")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        # 1. Cadastrar medicamento CONTROLADO
        repo = MedicamentoRepositoryPostgres(session)
        cadastrar_use_case = CadastrarMedicamentoUseCase(repo)
        
        medicamento = cadastrar_use_case.execute({
            "nome": "Rivotril 2mg",
            "principio_ativo": "Clonazepam",
            "preco": Decimal("45.90"),
            "estoque_minimo": 20,
            "requer_receita": True  # ← CONTROLADO!
        })
        
        print(f"💊 Medicamento: {medicamento.nome}")
        print(f"   Requer receita? {medicamento.requer_receita}")
        
        # 2. Tentar vender SEM receita
        print("\n🚫 Tentando vender SEM receita...")
        try:
            medicamento.validar_venda_controlada(receita=None)
            print("❌ ERRO: Deveria ter bloqueado!")
        except ValueError as e:
            print(f"✅ Venda bloqueada: {e}")
        
        # 3. Criar receita válida
        cpf_paciente = CPF("123.456.789-09")
        cpf_medico = CPF("987.654.321-00")
        
        receita = Receita(
            paciente_nome="Pedro Alves",
            paciente_cpf=cpf_paciente,
            medicamento_nome="Rivotril 2mg",
            quantidade=30,
            dosagem="1 comprimido 2x ao dia",
            medico_nome="Dr. Roberto Lima",
            medico_cpf=cpf_medico,
            medico_crm="789012/MG",
            data_emissao=date.today(),
            dias_validade=60  # Tarja preta = 60 dias
        )
        
        # 4. Vender COM receita
        print("\n✅ Tentando vender COM receita válida...")
        try:
            medicamento.validar_venda_controlada(receita)
            print("✅ Venda autorizada!")
        except ValueError as e:
            print(f"❌ ERRO inesperado: {e}")
        
    finally:
        session.close()
    
    print()


def teste_use_case_validar_receita():
    """Testa Use Case completo de validação"""
    print("🧪 Teste 6: Use Case Validar Receita")
    print("-" * 50)
    
    session = SessionLocal()
    
    try:
        # 1. Buscar medicamento controlado
        repo = MedicamentoRepositoryPostgres(session)
        medicamentos = repo.listar_todos()
        medicamento = next((m for m in medicamentos if m.requer_receita), None)
        
        if not medicamento:
            print("⚠️ Nenhum medicamento controlado encontrado. Pulando teste.")
            return
        
        print(f"💊 Testando com: {medicamento.nome}")
        
        # 2. Criar use case
        validar_use_case = ValidarReceitaUseCase(repo)
        
        # 3. Validar receita
        resultado = validar_use_case.execute(
            medicamento_id=medicamento.id,
            paciente_nome="Ana Paula Silva",
            paciente_cpf="12345678909",
            medicamento_nome=medicamento.nome,
            quantidade=30,
            dosagem="1 comprimido 2x ao dia",
            medico_nome="Dr. Fernando Dias",
            medico_cpf="98765432100",
            medico_crm="345678/SP",
            data_emissao=date.today().isoformat(),
            dias_validade=30
        )
        
        print(f"\n📋 Resultado da Validação:")
        print(f"   Válido? {resultado['valido']}")
        print(f"   Pode vender? {resultado['pode_vender']}")
        print(f"   Mensagem: {resultado['mensagem']}")
        
        if resultado.get('receita'):
            print(f"   Paciente: {resultado['receita']['paciente']}")
            print(f"   Médico: {resultado['receita']['medico']}")
            print(f"   Válida até: {resultado['receita']['valida_ate']}")
        
    finally:
        session.close()
    
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 TESTES DE VALIDAÇÕES COMPLEXAS")
    print("=" * 50)
    print()
    
    # Limpar banco
    limpar_banco()
    
    # Testes de Value Objects
    teste_cpf_valido()
    teste_cpf_invalido()
    teste_receita_valida()
    teste_receita_vencida()
    
    # Testes de Validação Composta
    teste_validar_medicamento_controlado()
    teste_use_case_validar_receita()
    
    print("=" * 50)
    print("✅ Todos os testes concluídos!")
    print("=" * 50)
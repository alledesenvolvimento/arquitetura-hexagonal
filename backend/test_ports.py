"""
Testes dos Ports (Interfaces) - Aula 5
Verifica se as interfaces estão bem definidas
"""

from abc import ABC
from src.domain.ports import (
    MedicamentoRepositoryPort,
    LoteRepositoryPort,
    EstoqueServicePort
)


def teste_medicamento_repository_port_e_interface():
    """Testa se MedicamentoRepositoryPort é uma interface abstrata"""
    print("🧪 Teste 1: MedicamentoRepositoryPort é interface?")
    
    # Verificar se é abstrata
    assert issubclass(MedicamentoRepositoryPort, ABC)
    print("✅ MedicamentoRepositoryPort é ABC (classe abstrata)")
    
    # Verificar métodos abstratos
    metodos_esperados = [
        'salvar',
        'buscar_por_id',
        'listar_todos',
        'atualizar',
        'deletar'
    ]
    
    metodos_port = [m for m in dir(MedicamentoRepositoryPort) if not m.startswith('_')]
    
    for metodo in metodos_esperados:
        assert metodo in metodos_port, f"Método {metodo} não encontrado!"
        print(f"   ✅ Método '{metodo}' encontrado")
    
    print()


def teste_lote_repository_port_e_interface():
    """Testa se LoteRepositoryPort é uma interface abstrata"""
    print("🧪 Teste 2: LoteRepositoryPort é interface?")
    
    # Verificar se é abstrata
    assert issubclass(LoteRepositoryPort, ABC)
    print("✅ LoteRepositoryPort é ABC (classe abstrata)")
    
    # Verificar métodos abstratos
    metodos_esperados = [
        'salvar',
        'buscar_por_id',
        'listar_todos',
        'buscar_por_medicamento',
        'listar_vencendo_em',
        'atualizar',
        'deletar'
    ]
    
    metodos_port = [m for m in dir(LoteRepositoryPort) if not m.startswith('_')]
    
    for metodo in metodos_esperados:
        assert metodo in metodos_port, f"Método {metodo} não encontrado!"
        print(f"   ✅ Método '{metodo}' encontrado")
    
    print()


def teste_estoque_service_port_e_interface():
    """Testa se EstoqueServicePort é uma interface abstrata"""
    print("🧪 Teste 3: EstoqueServicePort é interface?")
    
    # Verificar se é abstrata
    assert issubclass(EstoqueServicePort, ABC)
    print("✅ EstoqueServicePort é ABC (classe abstrata)")
    
    # Verificar métodos abstratos
    metodos_esperados = [
        'verificar_disponibilidade',
        'registrar_entrada',
        'registrar_saida',
        'consultar_estoque_atual',
        'listar_estoque_baixo'
    ]
    
    metodos_port = [m for m in dir(EstoqueServicePort) if not m.startswith('_')]
    
    for metodo in metodos_esperados:
        assert metodo in metodos_port, f"Método {metodo} não encontrado!"
        print(f"   ✅ Método '{metodo}' encontrado")
    
    print()


def teste_nao_pode_instanciar_ports():
    """Testa que não consegue instanciar Ports diretamente"""
    print("🧪 Teste 4: Ports não podem ser instanciados")
    
    # Tentar instanciar MedicamentoRepositoryPort
    try:
        port = MedicamentoRepositoryPort()
        print("❌ ERRO: MedicamentoRepositoryPort deveria ser abstrato!")
        assert False, "Não deveria conseguir instanciar!"
    except TypeError as e:
        print(f"✅ MedicamentoRepositoryPort não pode ser instanciado: {type(e).__name__}")
    
    # Tentar instanciar LoteRepositoryPort
    try:
        port = LoteRepositoryPort()
        print("❌ ERRO: LoteRepositoryPort deveria ser abstrato!")
        assert False, "Não deveria conseguir instanciar!"
    except TypeError as e:
        print(f"✅ LoteRepositoryPort não pode ser instanciado: {type(e).__name__}")
    
    # Tentar instanciar EstoqueServicePort
    try:
        port = EstoqueServicePort()
        print("❌ ERRO: EstoqueServicePort deveria ser abstrato!")
        assert False, "Não deveria conseguir instanciar!"
    except TypeError as e:
        print(f"✅ EstoqueServicePort não pode ser instanciado: {type(e).__name__}")
    
    print()


def teste_imports_funcionam():
    """Testa se os imports estão corretos"""
    print("🧪 Teste 5: Imports funcionam corretamente?")
    
    # Importar do __init__.py
    from src.domain.ports import (
        MedicamentoRepositoryPort,
        LoteRepositoryPort,
        EstoqueServicePort
    )
    
    print("✅ MedicamentoRepositoryPort importado")
    print("✅ LoteRepositoryPort importado")
    print("✅ EstoqueServicePort importado")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTANDO PORTS (INTERFACES) - AULA 5")
    print("=" * 60)
    print()
    
    teste_medicamento_repository_port_e_interface()
    teste_lote_repository_port_e_interface()
    teste_estoque_service_port_e_interface()
    teste_nao_pode_instanciar_ports()
    teste_imports_funcionam()
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
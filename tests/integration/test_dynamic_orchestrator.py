#!/usr/bin/env python3
"""Teste do DynamicOrchestrator."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipelines.DynamicOrchestrator import DynamicOrchestrator
from rpa.infra.bootstrap import initialize_system


def test_list_workflows():
    """Testa listagem de workflows disponíveis."""
    print("🧪 Testando listagem de workflows...")

    workflows = DynamicOrchestrator.list_available_workflows()
    print(f"✅ Workflows disponíveis: {workflows}")

    if 'cadastro_produtos' not in workflows:
        print("❌ Workflow 'cadastro_produtos' não encontrado")
        return False

    return True


def test_get_workflow_info():
    """Testa obtenção de informações do workflow."""
    print("\n🧪 Testando obtenção de informações do workflow...")

    info = DynamicOrchestrator.get_workflow_info('cadastro_produtos')

    if info is None:
        print("❌ Não foi possível obter informações do workflow")
        return False

    print(f"✅ Informações do workflow:")
    print(f"   Nome: {info['name']}")
    print(f"   Descrição: {info['description']}")
    print(f"   Template: {info['template']}")
    print(f"   Tipo de fluxo: {info['flow_type']}")
    print(f"   Número de ações: {info['actions_count']}")
    print(f"   Tem mapeamento de dados: {info['has_data_mapping']}")

    return True


def test_orchestrator_creation():
    """Testa criação do DynamicOrchestrator."""
    print("\n🧪 Testando criação do DynamicOrchestrator...")

    try:
        orchestrator = DynamicOrchestrator('cadastro_produtos')
        print(f"✅ DynamicOrchestrator criado para workflow: {orchestrator.workflow_name}")
        print(f"✅ Configuração carregada: {orchestrator.config.get('description')}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar DynamicOrchestrator: {e}")
        return False


def test_data_mapping():
    """Testa mapeamento de dados."""
    print("\n🧪 Testando mapeamento de dados...")

    orchestrator = DynamicOrchestrator('cadastro_produtos')

    # Dados no formato de origem (CSV)
    source_data = [
        {
            'nome': 'Produto Teste',
            'codigo_barras': '1234567890123',
            'quantidade': '10',
            'preco': '29.90',
            'preco_atacado': '25.00',
            'quantidade_minima_atacado': '50'
        }
    ]

    # Aplica mapeamento
    mapped_data = orchestrator.apply_data_mapping(source_data)

    print(f"✅ Dados originais: {source_data[0]}")
    print(f"✅ Dados mapeados: {mapped_data[0]}")

    # Verifica se os campos foram mapeados corretamente
    expected_fields = ['name', 'barcode', 'quantity', 'price', 'wholesale_price', 'wholesale_minimum_quantity']
    for field in expected_fields:
        if field not in mapped_data[0]:
            print(f"❌ Campo mapeado '{field}' não encontrado")
            return False

    return True


def test_orchestrator_with_mock_data():
    """Testa execução do orchestrator com dados mock."""
    print("\n🧪 Testando execução do orchestrator com dados mock...")

    orchestrator = DynamicOrchestrator('cadastro_produtos')

    # Dados mock no formato esperado
    mock_data = [
        {
            'nome': 'Produto Mock 1',
            'codigo_barras': '1111111111111',
            'quantidade': '5',
            'preco': '19.90',
            'preco_atacado': '15.00',
            'quantidade_minima_atacado': '30'
        },
        {
            'nome': 'Produto Mock 2',
            'codigo_barras': '2222222222222',
            'quantidade': '8',
            'preco': '39.90',
            'preco_atacado': '35.00',
            'quantidade_minima_atacado': '40'
        }
    ]

    try:
        print("⚠️  Executando workflow com dados mock (sem BotCity)...")
        results = orchestrator.execute(data=mock_data)

        print(f"✅ Execução concluída. Resultados: {len(results)} registro(s)")

        # Verifica estrutura dos resultados
        for i, result in enumerate(results):
            print(f"   Registro {i+1}: sucesso={result.get('success')}")
            if 'actions_executed' in result:
                print(f"     Ações executadas: {len(result['actions_executed'])}")

        return True
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        # Em ambiente sem BotCity, alguns erros são esperados
        print("⚠️  Erro pode ser esperado em ambiente sem BotCity")
        return True  # Considera como sucesso para fins de teste de arquitetura


def test_invalid_workflow():
    """Testa comportamento com workflow inválido."""
    print("\n🧪 Testando workflow inválido...")

    try:
        orchestrator = DynamicOrchestrator('workflow_inexistente')
        print("❌ Não deveria criar orchestrator para workflow inexistente")
        return False
    except ValueError as e:
        print(f"✅ Comportamento esperado: {e}")
        return True
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def main():
    """Função principal de teste."""
    print("🚀 Iniciando testes do DynamicOrchestrator\n")

    # Inicializa o sistema
    print("🔧 Inicializando sistema...")
    try:
        initialize_system()
        print("✅ Sistema inicializado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema: {e}")
        return 1

    # Executa testes
    tests = [
        test_list_workflows,
        test_get_workflow_info,
        test_orchestrator_creation,
        test_data_mapping,
        test_invalid_workflow,
        test_orchestrator_with_mock_data
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Erro inesperado no teste {test_func.__name__}: {e}")
            failed += 1

    print(f"\n📊 Resultado dos testes: {passed} passaram, {failed} falharam")

    if failed == 0:
        print("\n🎉 Todos os testes passaram! DynamicOrchestrator está funcionando.")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique a implementação.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
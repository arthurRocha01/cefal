#!/usr/bin/env python3
"""Teste da nova arquitetura do CeFal."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rpa.infra.bootstrap import initialize_system
from rpa.flows.generic_flow import GenericFlow


def test_generic_flow_creation():
    """Testa criação de GenericFlow a partir do nome do workflow."""
    print("🧪 Testando criação de GenericFlow...")

    # Dados de teste no formato novo
    test_data = [
        {
            'nome': 'Produto Teste 1',
            'codigo_barras': '1234567890123',
            'quantidade': '10',
            'preco': '29.90',
            'preco_atacado': '25.00',
            'quantidade_minima_atacado': '50'
        },
        {
            'nome': 'Produto Teste 2',
            'codigo_barras': '9876543210987',
            'quantidade': '5',
            'preco': '49.90',
            'preco_atacado': '40.00',
            'quantidade_minima_atacado': '30'
        }
    ]

    try:
        # Cria fluxo a partir do nome do workflow
        flow = GenericFlow.from_workflow_name('cadastro_produtos', test_data)
        print("✅ GenericFlow criado com sucesso")

        # Verifica configuração
        print(f"📋 Configuração carregada: {flow.config.get('description')}")
        print(f"📋 Ações configuradas: {len(flow.actions)}")

        # Verifica mapeamento de dados
        print(f"📋 Mapeamento de dados: {flow.data_mapping}")

        return True
    except Exception as e:
        print(f"❌ Erro ao criar GenericFlow: {e}")
        return False


def test_workflow_configuration():
    """Testa configuração do workflow."""
    print("\n🧪 Testando configuração do workflow...")

    from config.workflows import WORKFLOWS

    if 'cadastro_produtos' not in WORKFLOWS:
        print("❌ Workflow 'cadastro_produtos' não encontrado")
        return False

    config = WORKFLOWS['cadastro_produtos']

    # Verifica campos obrigatórios
    required_fields = ['template', 'description', 'actions', 'data_mapping']
    for field in required_fields:
        if field not in config:
            print(f"❌ Campo obrigatório '{field}' não encontrado no workflow")
            return False

    print(f"✅ Workflow configurado: {config['description']}")
    print(f"✅ Template: {config['template']}")
    print(f"✅ Número de ações: {len(config['actions'])}")

    # Verifica ações
    action_types = [action['type'] for action in config['actions']]
    print(f"✅ Tipos de ação: {action_types}")

    return True


def test_action_factory():
    """Testa se a ActionFactory está funcionando."""
    print("\n🧪 Testando ActionFactory...")

    from rpa.actions.action_factory import ActionFactory

    # Inicializa a factory
    ActionFactory.initialize()

    # Verifica ações registradas
    registered_actions = ActionFactory.get_registered_actions()
    print(f"✅ Ações registradas: {registered_actions}")

    # Verifica se ações necessárias estão registradas
    required_actions = ['click', 'type']
    for action in required_actions:
        if action not in registered_actions:
            print(f"❌ Ação '{action}' não registrada")
            return False

    print("✅ ActionFactory funcionando corretamente")
    return True


def test_compatibility_function():
    """Testa função de compatibilidade register_products."""
    print("\n🧪 Testando função de compatibilidade...")

    from rpa.flows.register_product import register_products

    # Dados no formato antigo
    old_format_data = [
        {
            'name': 'Produto Compatibilidade 1',
            'barcode': '1111111111111',
            'quantity': '15',
            'price': '39.90',
            'wholesale_price': '35.00',
            'wholesale_minimum_quantity': '40'
        }
    ]

    try:
        print("⚠️  Chamando função de compatibilidade register_products()...")
        # Nota: Esta função não executará ações reais sem o ambiente BotCity
        # mas deve criar o GenericFlow corretamente
        results = register_products(old_format_data)
        print("✅ Função de compatibilidade chamada com sucesso")
        print(f"✅ Resultados: {len(results)} registro(s) processado(s)")
        return True
    except Exception as e:
        print(f"❌ Erro na função de compatibilidade: {e}")
        return False


def main():
    """Função principal de teste."""
    print("🚀 Iniciando testes da nova arquitetura CeFal\n")

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
        test_action_factory,
        test_workflow_configuration,
        test_generic_flow_creation,
        test_compatibility_function
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
        print("\n🎉 Todos os testes passaram! Nova arquitetura está funcionando.")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique a implementação.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
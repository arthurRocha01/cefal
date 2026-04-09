#!/usr/bin/env python3
"""Testes para a CLI do CeFal."""

import sys
import os
import subprocess
import tempfile
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rpa.infra.bootstrap import initialize_system


def test_cli_list() -> bool:
    """Testa o comando --list da CLI."""
    print("🧪 Testando comando --list...")

    try:
        # Executa CLI com --list
        result = subprocess.run(
            [sys.executable, 'cli.py', '--list'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        print(f"📋 Saída do comando --list:")
        print(result.stdout)

        if result.returncode != 0:
            print(f"❌ Comando --list falhou com código {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False

        # Verifica se a saída contém o workflow esperado
        if 'cadastro_produtos' not in result.stdout:
            print("❌ Workflow 'cadastro_produtos' não listado")
            return False

        print("✅ Comando --list funcionando corretamente")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar --list: {e}")
        return False


def test_cli_list_verbose() -> bool:
    """Testa o comando --list --verbose da CLI."""
    print("\n🧪 Testando comando --list --verbose...")

    try:
        # Executa CLI com --list --verbose
        result = subprocess.run(
            [sys.executable, 'cli.py', '--list', '--verbose'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        print(f"📋 Saída do comando --list --verbose:")
        print(result.stdout)

        if result.returncode != 0:
            print(f"❌ Comando --list --verbose falhou com código {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False

        # Verifica se a saída contém informações detalhadas
        expected_info = ['Descrição:', 'Template:', 'Tipo:', 'Ações:', 'Mapeamento de dados:']
        for info in expected_info:
            if info not in result.stdout:
                print(f"❌ Informação '{info}' não encontrada na saída verbosa")
                return False

        print("✅ Comando --list --verbose funcionando corretamente")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar --list --verbose: {e}")
        return False


def test_cli_help() -> bool:
    """Testa o comando --help da CLI."""
    print("\n🧪 Testando comando --help...")

    try:
        # Executa CLI com --help
        result = subprocess.run(
            [sys.executable, 'cli.py', '--help'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        print(f"📋 Saída do comando --help:")
        print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)

        if result.returncode != 0:
            print(f"❌ Comando --help falhou com código {result.returncode}")
            print(f"Stderr: {result.stderr}")
            return False

        # Verifica se a saída contém informações de ajuda
        expected_help = ['usage:', '--help', '--list', '--verbose', '--data', 'Exemplos:']
        for help_text in expected_help:
            if help_text.lower() not in result.stdout.lower():
                print(f"❌ Texto de ajuda '{help_text}' não encontrado")
                return False

        print("✅ Comando --help funcionando corretamente")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar --help: {e}")
        return False


def test_cli_invalid_workflow() -> bool:
    """Testa comportamento com workflow inválido."""
    print("\n🧪 Testando workflow inválido...")

    try:
        # Executa CLI com workflow inexistente
        result = subprocess.run(
            [sys.executable, 'cli.py', 'workflow_inexistente'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        print(f"📋 Saída para workflow inválido:")
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")

        # O comando deve falhar com código de erro
        if result.returncode == 0:
            print("❌ Comando com workflow inválido deveria falhar")
            return False

        # Verifica se a mensagem de erro é apropriada
        if 'não encontrado' not in result.stdout.lower() and 'use --list' not in result.stdout.lower():
            print("❌ Mensagem de erro inadequada para workflow inválido")
            return False

        print("✅ Comportamento correto para workflow inválido")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar workflow inválido: {e}")
        return False


def test_cli_no_command() -> bool:
    """Testa comportamento sem nenhum comando."""
    print("\n🧪 Testando execução sem comandos...")

    try:
        # Executa CLI sem argumentos
        result = subprocess.run(
            [sys.executable, 'cli.py'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        print(f"📋 Saída sem comandos:")
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")

        # O comando deve falhar com código de erro
        if result.returncode == 0:
            print("❌ CLI sem comandos deveria falhar")
            return False

        # Verifica se mostra ajuda
        if 'use --help' not in result.stdout.lower():
            print("❌ Não sugeriu usar --help")
            return False

        print("✅ Comportamento correto sem comandos")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar sem comandos: {e}")
        return False


def create_test_csv() -> str:
    """Cria um arquivo CSV de teste temporário."""
    import csv

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['nome', 'codigo_barras', 'quantidade', 'preco', 'preco_atacado', 'quantidade_minima_atacado'])
        writer.writerow(['Produto Teste CSV 1', '3333333333333', '15', '39.90', '35.00', '40'])
        writer.writerow(['Produto Teste CSV 2', '4444444444444', '8', '59.90', '50.00', '25'])
        return f.name


def test_cli_with_test_data() -> bool:
    """Testa execução com --test-data."""
    print("\n🧪 Testando execução com --test-data...")

    try:
        # Executa CLI com --test-data
        result = subprocess.run(
            [sys.executable, 'cli.py', 'cadastro_produtos', '--test-data'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        print(f"📋 Saída com --test-data:")
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")

        # Em ambiente sem BotCity, alguns erros são esperados
        # Mas a CLI deve tentar executar
        if 'Iniciando execução' not in result.stdout:
            print("❌ Não iniciou execução do workflow")
            return False

        print("✅ Comando --test-data funcionando (erros de BotCity são esperados)")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar --test-data: {e}")
        return False


def main() -> int:
    """Função principal de teste."""
    print("🚀 Iniciando testes da CLI do CeFal\n")

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
        test_cli_list,
        test_cli_list_verbose,
        test_cli_help,
        test_cli_invalid_workflow,
        test_cli_no_command,
        test_cli_with_test_data
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
        print("\n🎉 Todos os testes da CLI passaram!")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique a implementação.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
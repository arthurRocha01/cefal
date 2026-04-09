#!/usr/bin/env python3
"""Interface de linha de comando para o CeFal.

Esta CLI permite executar workflows configurados na nova arquitetura genérica.
"""

import sys
import os
import argparse
from typing import List, Dict, Any

# Adiciona o diretório atual ao path para importações
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipelines.DynamicOrchestrator import DynamicOrchestrator
from rpa.infra.bootstrap import initialize_system
from utils.logging import get_logger


def list_workflows(verbose: bool = False) -> None:
    """Lista todos os workflows disponíveis.

    Args:
        verbose: Se True, mostra informações detalhadas de cada workflow
    """
    logger = get_logger('cli')
    logger.info("Listando workflows disponíveis")

    workflows = DynamicOrchestrator.list_available_workflows()

    if not workflows:
        logger.error("Nenhum workflow configurado")
        print("❌ Nenhum workflow configurado.")
        print("   Configure workflows em config/workflows.py")
        return

    logger.info(f"Encontrados {len(workflows)} workflows")
    print("📋 Workflows disponíveis no CeFal:\n")

    for workflow_name in workflows:
        if verbose:
            info = DynamicOrchestrator.get_workflow_info(workflow_name)
            if info:
                print(f"🔹 {workflow_name}")
                print(f"   Descrição: {info['description']}")
                print(f"   Template: {info['template']}")
                print(f"   Tipo: {info['flow_type']}")
                print(f"   Ações: {info['actions_count']}")
                print(f"   Mapeamento de dados: {'Sim' if info['has_data_mapping'] else 'Não'}")
                print()
        else:
            info = DynamicOrchestrator.get_workflow_info(workflow_name)
            if info:
                print(f"🔹 {workflow_name} - {info['description']}")
            else:
                print(f"🔹 {workflow_name}")


def execute_workflow(workflow_name: str, data_file: str = None, data: List[Dict] = None) -> bool:
    """Executa um workflow específico.

    Args:
        workflow_name: Nome do workflow a ser executado
        data_file: Caminho para arquivo de dados (CSV/XLSX)
        data: Dados já carregados em memória

    Returns:
        True se a execução foi bem-sucedida, False caso contrário
    """
    logger = get_logger('cli')
    try:
        logger.info(f"Iniciando execução do workflow: {workflow_name}")
        print(f"🚀 Iniciando execução do workflow: {workflow_name}")

        # Verifica se o workflow existe
        if workflow_name not in DynamicOrchestrator.list_available_workflows():
            logger.error(f"Workflow '{workflow_name}' não encontrado")
            print(f"❌ Workflow '{workflow_name}' não encontrado.")
            print("   Use '--list' para ver workflows disponíveis.")
            return False

        # Cria o orchestrator
        orchestrator = DynamicOrchestrator(workflow_name)

        # Executa o workflow
        if data_file:
            logger.info(f"Executando com arquivo de dados: {data_file}")
            results = orchestrator.execute(data_file_path=data_file)
        elif data:
            logger.info(f"Executando com {len(data)} registros em memória")
            results = orchestrator.execute(data=data)
        else:
            logger.error("Nenhum dado fornecido para execução")
            print("❌ Nenhum dado fornecido para execução.")
            print("   Use --data <arquivo> ou forneça dados diretamente.")
            return False

        # Mostra resumo
        successes = sum(1 for r in results if r.get('success', False))
        failures = len(results) - successes

        logger.info(
            f"Execução concluída: {successes}/{len(results)} sucessos, {failures} falhas"
        )
        print(f"\n✅ Execução concluída com sucesso!")
        print(f"📊 Total de registros processados: {len(results)}")

        if successes > 0:
            print(f"✅ Registros com sucesso: {successes}")
        if failures > 0:
            print(f"❌ Registros com falha: {failures}")

        return True

    except Exception as e:
        logger.error(f"Erro durante execução do workflow: {e}")
        print(f"❌ Erro durante execução do workflow: {e}")
        return False


def create_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        description='CeFal - Framework RPA Genérico',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --list                    Lista workflows disponíveis
  %(prog)s --list --verbose          Lista com informações detalhadas
  %(prog)s cadastro_produtos --data produtos.csv  Executa workflow

Para mais informações, consulte a documentação em docs/.
        """
    )

    # Comando principal (workflow a ser executado)
    parser.add_argument(
        'workflow',
        nargs='?',
        help='Nome do workflow a ser executado'
    )

    # Opções gerais
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Lista todos os workflows disponíveis'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verboso (mostra mais informações)'
    )

    # Opções para execução
    parser.add_argument(
        '--data', '-d',
        type=str,
        help='Caminho para arquivo de dados (CSV/XLSX)'
    )

    # Opção para dados em memória (para testes)
    parser.add_argument(
        '--test-data',
        action='store_true',
        help='Usa dados de teste em memória (apenas para desenvolvimento)'
    )

    return parser


def get_test_data() -> List[Dict]:
    """Retorna dados de teste para desenvolvimento."""
    return [
        {
            'nome': 'Produto Teste CLI 1',
            'codigo_barras': '1111111111111',
            'quantidade': '10',
            'preco': '29.90',
            'preco_atacado': '25.00',
            'quantidade_minima_atacado': '50'
        },
        {
            'nome': 'Produto Teste CLI 2',
            'codigo_barras': '2222222222222',
            'quantidade': '5',
            'preco': '49.90',
            'preco_atacado': '40.00',
            'quantidade_minima_atacado': '30'
        }
    ]


def main() -> int:
    """Função principal da CLI."""
    logger = get_logger('cli')
    parser = create_parser()
    args = parser.parse_args()

    # Inicializa o sistema
    try:
        logger.info("Inicializando sistema CeFal")
        print("🔧 Inicializando sistema CeFal...")
        initialize_system()
        logger.info("Sistema inicializado com sucesso")
        print("✅ Sistema inicializado com sucesso\n")
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema: {e}")
        print(f"❌ Erro ao inicializar sistema: {e}")
        return 1

    # Modo listagem
    if args.list:
        logger.info("Executando modo listagem")
        list_workflows(verbose=args.verbose)
        return 0

    # Modo execução
    if args.workflow:
        logger.info(f"Executando workflow: {args.workflow}")
        if args.test_data:
            # Usa dados de teste
            logger.info("Usando dados de teste")
            test_data = get_test_data()
            success = execute_workflow(args.workflow, data=test_data)
        else:
            # Usa arquivo de dados ou erro
            if args.data:
                logger.info(f"Usando arquivo de dados: {args.data}")
            success = execute_workflow(args.workflow, data_file=args.data)

        return 0 if success else 1

    # Nenhum comando válido fornecido
    logger.error("Nenhum comando válido fornecido")
    print("❌ Nenhum comando válido fornecido.")
    print("   Use --help para ver opções disponíveis.")
    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
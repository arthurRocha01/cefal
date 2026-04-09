"""Orchestrator dinâmico para execução de workflows no CeFal.

Este módulo implementa um orchestrator que pode carregar e executar qualquer
workflow configurado no sistema, usando a nova arquitetura genérica.
"""

from typing import List, Dict, Any, Optional
from interface.ProcessInterface import ProcessInterface
from config.workflows import WORKFLOWS
from rpa.flows.generic_flow import GenericFlow
from rpa.infra.bootstrap import prepare_workflow_execution
from utils.logging import get_logger


class DynamicOrchestrator:
    """Orchestrator dinâmico para execução de workflows configurados."""

    def __init__(self, workflow_name: str):
        """
        Inicializa o orchestrator para um workflow específico.

        Args:
            workflow_name (str): Nome do workflow a ser executado

        Raises:
            ValueError: Se o workflow não existir
        """
        self.workflow_name = workflow_name
        self.logger = get_logger(workflow_name)
        self.config = self.load_workflow_config(workflow_name)
        self.process_interface = ProcessInterface()

    def load_workflow_config(self, workflow_name: str) -> Dict:
        """
        Carrega configuração do workflow especificado.

        Args:
            workflow_name (str): Nome do workflow

        Returns:
            dict: Configuração do workflow

        Raises:
            ValueError: Se o workflow não existir
        """
        if workflow_name not in WORKFLOWS:
            self.logger.error(f"Workflow '{workflow_name}' não encontrado")
            raise ValueError(f"Workflow '{workflow_name}' não encontrado")

        self.logger.info(f"Configuração do workflow '{workflow_name}' carregada")
        return WORKFLOWS[workflow_name]

    def get_flow_class(self):
        """
        Obtém a classe do fluxo baseado na configuração.

        Returns:
            class: Classe do fluxo a ser usado

        Note:
            Atualmente sempre retorna GenericFlow, mas pode ser estendido
            para suportar fluxos especializados baseados em 'flow_type'
        """
        # Por enquanto, sempre usa GenericFlow
        # Futuramente pode usar registry pattern baseado em flow_type
        return GenericFlow

    def apply_data_mapping(self, data: List[Dict]) -> List[Dict]:
        """
        Aplica mapeamento de dados se configurado no workflow.

        Args:
            data (list): Dados originais

        Returns:
            list: Dados mapeados conforme configuração
        """
        if 'data_mapping' not in self.config:
            return data

        mapping = self.config['data_mapping'].get('field_mapping', {})
        if not mapping:
            self.logger.debug("Mapeamento de dados vazio, retornando dados originais")
            return data

        mapped_data = []
        self.logger.info(f"Aplicando mapeamento de {len(mapping)} campos")

        for item_idx, item in enumerate(data):
            mapped_item = {}
            for source_field, target_field in mapping.items():
                if source_field in item:
                    mapped_item[target_field] = item[source_field]
                else:
                    mapped_item[target_field] = ''
                    self.logger.warning(
                        f"Campo de origem '{source_field}' não encontrado nos dados",
                        field=source_field
                    )
            mapped_data.append(mapped_item)

        self.logger.info(f"Mapeamento concluído: {len(mapped_data)} registros processados")
        return mapped_data

    def execute(self, data_file_path: Optional[str] = None, data: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Executa o workflow especificado.

        Args:
            data_file_path (str, optional): Caminho do arquivo de dados
            data (list, optional): Dados já carregados

        Returns:
            list: Resultados da execução

        Raises:
            ValueError: Se nenhum dado for fornecido
        """
        self.logger.start_workflow(self.config)

        # Carrega dados
        if data is None and data_file_path:
            self.logger.info(f"Carregando dados de: {data_file_path}")
            data = self.process_interface.read_data(data_file_path)
        elif data is None:
            self.logger.error("Nenhum dado fornecido para execução")
            raise ValueError("Nenhum dado fornecido para execução")

        self.logger.info(f"Dados carregados: {len(data)} registro(s)")

        # Aplica mapeamento de dados se configurado
        if 'data_mapping' in self.config:
            self.logger.info("Aplicando mapeamento de dados...")
            data = self.apply_data_mapping(data)

        # Prepara execução do workflow (carrega imagens, etc.)
        self.logger.info("Preparando execução do workflow...")
        workflow_config = prepare_workflow_execution(self.workflow_name)

        # Obtém classe do fluxo
        FlowClass = self.get_flow_class()
        self.logger.info(f"Usando classe de fluxo: {FlowClass.__name__}")

        # Cria e executa o fluxo
        flow = FlowClass(workflow_config, data)

        # Executa fluxo principal
        self.logger.info("Executando workflow...")
        results = flow.execute()

        # Retorna resumo
        summary = flow.get_summary()
        self.logger.info(
            f"Workflow concluído. Resumo: {summary['successful_records']}/{summary['total_records']} sucessos "
            f"({summary['success_rate']:.1f}%)"
        )

        return results

    @staticmethod
    def list_available_workflows() -> List[str]:
        """
        Lista todos os workflows disponíveis.

        Returns:
            list: Nomes dos workflows disponíveis
        """
        return list(WORKFLOWS.keys())

    @staticmethod
    def get_workflow_info(workflow_name: str) -> Optional[Dict]:
        """
        Obtém informações detalhadas sobre um workflow.

        Args:
            workflow_name (str): Nome do workflow

        Returns:
            dict or None: Informações do workflow ou None se não existir
        """
        if workflow_name not in WORKFLOWS:
            return None

        config = WORKFLOWS[workflow_name]
        return {
            'name': workflow_name,
            'description': config.get('description', 'Sem descrição'),
            'template': config.get('template', 'N/A'),
            'flow_type': config.get('flow_type', 'generic'),
            'steps': config.get('steps', []),
            'actions_count': len(config.get('actions', [])),
            'has_data_mapping': 'data_mapping' in config
        }
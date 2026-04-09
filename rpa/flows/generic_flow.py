"""Implementação concreta de fluxo genérico para o CeFal.

Este módulo implementa a classe GenericFlow que pode executar qualquer
workflow configurado no sistema, usando a ActionFactory para criar e
executar ações dinamicamente.
"""

from typing import Dict, List, Any, Optional
from rpa.flows.base_flow import BaseFlow
from rpa.actions.action_factory import ActionFactory
from rpa.infra.bootstrap import prepare_workflow_execution
from utils.logging import get_logger


class GenericFlow(BaseFlow):
    """Fluxo genérico que executa workflows baseados em configuração."""

    def __init__(self, workflow_config: Dict, data: List[Dict]):
        """
        Inicializa o fluxo genérico.

        Args:
            workflow_config (dict): Configuração completa do workflow
            data (list): Dados a serem processados (lista de registros)
        """
        super().__init__(workflow_config, data)
        self.actions = self.get_actions()
        self.data_mapping = workflow_config.get('data_mapping', {})
        self.results = []

        # Inicializa logger
        workflow_name = workflow_config.get('name', 'unknown')
        self.logger = get_logger(workflow_name)

    def execute(self) -> List[Dict]:
        """
        Executa o workflow completo.

        Returns:
            list: Lista de resultados para cada registro processado
        """
        workflow_desc = self.config.get('description', 'Desconhecido')
        self.logger.info(f"Iniciando execução do workflow: {workflow_desc}")

        # 1. Executa passos iniciais
        self.execute_initial_steps()

        # 2. Processa cada registro de dados
        for record_idx, record in enumerate(self.data):
            self.logger.info(f"Processando registro {record_idx + 1}/{len(self.data)}")

            try:
                result = self._process_record(record)
                self.results.append(result)
                self.logger.info(f"Registro {record_idx + 1} processado com sucesso")
            except Exception as e:
                self.logger.error(f"Erro ao processar registro {record_idx + 1}", error=e)
                self.results.append({
                    'record_index': record_idx,
                    'success': False,
                    'error': str(e),
                    'record': record
                })

        successful = len([r for r in self.results if r.get('success')])
        self.logger.info(f"Workflow concluído. {successful}/{len(self.results)} registros processados com sucesso")
        return self.results

    def _process_record(self, record: Dict) -> Dict:
        """
        Processa um único registro de dados.

        Args:
            record (dict): Dados do registro a ser processado

        Returns:
            dict: Resultado do processamento
        """
        result = {
            'record': record,
            'success': True,
            'actions_executed': [],
            'errors': []
        }

        # Mapeia dados do registro para campos do workflow
        mapped_data = self._map_record_data(record)

        # Executa cada ação configurada
        for action_config in self.actions:
            try:
                action_result = self._execute_action(action_config, mapped_data)
                result['actions_executed'].append({
                    'action': action_config.get('type'),
                    'field': action_config.get('field'),
                    'success': True,
                    'result': action_result
                })
            except Exception as e:
                result['success'] = False
                result['errors'].append({
                    'action': action_config.get('type'),
                    'field': action_config.get('field'),
                    'error': str(e)
                })
                print(f"   ❌ Erro na ação {action_config.get('type')} no campo {action_config.get('field')}: {e}")

                # Se a ação é obrigatória, interrompe o processamento deste registro
                if action_config.get('required', False):
                    raise

        return result

    def _execute_action(self, action_config: Dict, mapped_data: Dict) -> Any:
        """
        Executa uma ação específica.

        Args:
            action_config (dict): Configuração da ação
            mapped_data (dict): Dados mapeados para campos

        Returns:
            any: Resultado da execução da ação
        """
        action_type = action_config.get('type')
        field = action_config.get('field')

        if not action_type:
            raise ValueError("Configuração de ação sem tipo")

        if not field:
            raise ValueError("Configuração de ação sem campo")

        # Obtém valor do campo (pode ser do mapeamento ou valor fixo)
        value = self._get_action_value(action_config, mapped_data)

        # Cria e executa a ação
        action = ActionFactory.create_action(action_type, action_config)
        return action.execute(field, value)

    def _get_action_value(self, action_config: Dict, mapped_data: Dict) -> Optional[str]:
        """
        Obtém valor para uma ação a partir dos dados mapeados.

        Args:
            action_config (dict): Configuração da ação
            mapped_data (dict): Dados mapeados

        Returns:
            str or None: Valor para a ação
        """
        field = action_config.get('field')

        # Verifica se há valor fixo na configuração
        if 'value' in action_config:
            return action_config['value']

        # Tenta obter valor dos dados mapeados
        if field in mapped_data:
            return mapped_data[field]

        # Para ações de click que não precisam de valor
        if action_config.get('type') == 'click':
            return None

        # Se é obrigatório e não tem valor, levanta erro
        if action_config.get('required', False):
            raise ValueError(f"Campo obrigatório '{field}' não encontrado nos dados")

        return None

    def _map_record_data(self, record: Dict) -> Dict:
        """
        Mapeia dados do registro para campos do workflow.

        Args:
            record (dict): Dados do registro original

        Returns:
            dict: Dados mapeados para campos do workflow
        """
        mapped_data = {}

        # Obtém mapeamento de campos da configuração
        field_mapping = self.data_mapping.get('field_mapping', {})

        # Mapeia cada campo
        for source_field, target_field in field_mapping.items():
            if source_field in record:
                mapped_data[target_field] = record[source_field]
            else:
                print(f"   ⚠️ Campo de origem '{source_field}' não encontrado no registro")

        return mapped_data

    @classmethod
    def from_workflow_name(cls, workflow_name: str, data: List[Dict]) -> 'GenericFlow':
        """
        Cria um GenericFlow a partir do nome do workflow.

        Args:
            workflow_name (str): Nome do workflow
            data (list): Dados a serem processados

        Returns:
            GenericFlow: Instância do fluxo configurada

        Raises:
            ValueError: Se o workflow não existir
        """
        # Prepara a execução do workflow (carrega imagens, etc.)
        workflow_config = prepare_workflow_execution(workflow_name)

        # Cria e retorna a instância do fluxo
        return cls(workflow_config, data)

    def get_summary(self) -> Dict:
        """
        Retorna um resumo da execução.

        Returns:
            dict: Resumo com estatísticas da execução
        """
        successful = len([r for r in self.results if r.get('success')])
        failed = len(self.results) - successful

        total_actions = 0
        successful_actions = 0

        for result in self.results:
            if result.get('success'):
                successful_actions += len(result.get('actions_executed', []))
            total_actions += len(result.get('actions_executed', [])) + len(result.get('errors', []))

        return {
            'total_records': len(self.results),
            'successful_records': successful,
            'failed_records': failed,
            'total_actions': total_actions,
            'successful_actions': successful_actions,
            'success_rate': (successful / len(self.results)) * 100 if self.results else 0
        }
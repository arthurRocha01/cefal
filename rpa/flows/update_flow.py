"""Fluxo especializado para operações de atualização no CeFal.

Este fluxo otimiza operações de atualização com busca de registros existentes,
comparação de dados e atualização seletiva de campos.
"""

from typing import Dict, List, Any, Optional
from rpa.flows.base_flow import BaseFlow
from rpa.actions.action_factory import ActionFactory
from utils.logging import get_logger


class UpdateFlow(BaseFlow):
    """Fluxo especializado para operações de atualização."""

    def __init__(self, workflow_config: Dict, data: List[Dict]):
        """
        Inicializa o fluxo de atualização.

        Args:
            workflow_config (dict): Configuração do workflow
            data (list): Dados a serem processados (lista de registros)
        """
        super().__init__(workflow_config, data)
        self.actions = self.get_actions()
        self.data_mapping = workflow_config.get('data_mapping', {})
        self.results = []

        # Inicializa logger
        workflow_name = workflow_config.get('name', 'unknown')
        self.logger = get_logger(workflow_name)

        # Configurações específicas para atualização
        self.search_actions = workflow_config.get('search_actions', [])
        self.update_actions = workflow_config.get('update_actions', [])
        self.verify_changes = workflow_config.get('verify_changes', True)
        self.skip_unchanged = workflow_config.get('skip_unchanged', True)
        self.max_search_attempts = workflow_config.get('max_search_attempts', 3)

    def execute(self) -> List[Dict]:
        """
        Executa o fluxo de atualização completo.

        Returns:
            list: Lista de resultados para cada registro processado
        """
        workflow_desc = self.config.get('description', 'Atualização')
        self.logger.info(f"Iniciando fluxo de atualização: {workflow_desc}")
        self.logger.info(f"Total de registros: {len(self.data)}")

        # 1. Executa passos iniciais
        self.execute_initial_steps()

        # 2. Processa cada registro de dados
        for record_idx, record in enumerate(self.data):
            self.logger.info(f"Processando registro {record_idx + 1}/{len(self.data)}")

            try:
                result = self._process_update_record(record, record_idx)
                self.results.append(result)

                if result['success']:
                    if result.get('updated'):
                        self.logger.info(f"✅ Registro {record_idx + 1} atualizado com sucesso")
                    else:
                        self.logger.info(f"ℹ️ Registro {record_idx + 1} não necessitou atualização")
                else:
                    self.logger.warning(f"⚠️ Registro {record_idx + 1} falhou: {result.get('error', 'Erro desconhecido')}")

            except Exception as e:
                self.logger.error(f"❌ Erro crítico ao processar registro {record_idx + 1}", error=str(e))
                self.results.append({
                    'record_index': record_idx,
                    'success': False,
                    'error': str(e),
                    'record': record,
                    'updated': False,
                    'search_successful': False
                })

        # 3. Gera relatório final
        self._generate_update_report()

        return self.results

    def _process_update_record(self, record: Dict, record_idx: int) -> Dict:
        """
        Processa um registro para atualização.

        Args:
            record (dict): Dados do registro
            record_idx (int): Índice do registro

        Returns:
            dict: Resultado do processamento
        """
        result = {
            'record_index': record_idx,
            'record': record,
            'success': True,
            'updated': False,
            'search_successful': False,
            'search_actions': [],
            'update_actions': [],
            'changes_detected': [],
            'no_changes_needed': [],
            'errors': []
        }

        # 1. Mapeia dados do registro
        mapped_data = self._map_record_data(record)

        # 2. Busca registro existente
        search_result = self._search_existing_record(mapped_data)
        result['search_successful'] = search_result['success']
        result['search_actions'] = search_result['actions_executed']

        if not search_result['success']:
            result['success'] = False
            result['error'] = 'Registro não encontrado para atualização'
            result['errors'].extend(search_result['errors'])
            return result

        # 3. Verifica se há alterações necessárias
        if self.skip_unchanged:
            changes_needed = self._detect_changes_needed(mapped_data, search_result['current_values'])
            result['changes_detected'] = changes_needed

            if not changes_needed:
                result['no_changes_needed'] = ['Nenhuma alteração necessária']
                return result  # Registro não precisa ser atualizado

        # 4. Executa ações de atualização
        update_result = self._execute_update_actions(mapped_data)
        result['update_actions'] = update_result['actions_executed']
        result['updated'] = update_result['success']

        if not update_result['success']:
            result['success'] = False
            result['error'] = 'Falha na atualização do registro'
            result['errors'].extend(update_result['errors'])

        return result

    def _search_existing_record(self, mapped_data: Dict) -> Dict:
        """
        Busca registro existente no sistema.

        Args:
            mapped_data (dict): Dados mapeados para busca

        Returns:
            dict: Resultado da busca
        """
        result = {
            'success': False,
            'actions_executed': [],
            'current_values': {},
            'errors': []
        }

        # Executa ações de busca com múltiplas tentativas
        for attempt in range(self.max_search_attempts):
            try:
                search_result = self._execute_search_actions(mapped_data)
                result['actions_executed'] = search_result['actions_executed']
                result['current_values'] = search_result['current_values']
                result['success'] = True
                return result

            except Exception as e:
                self.logger.warning(f"Tentativa de busca {attempt + 1}/{self.max_search_attempts} falhou", error=str(e))
                result['errors'].append({
                    'attempt': attempt + 1,
                    'error': str(e)
                })

                if attempt == self.max_search_attempts - 1:
                    result['error'] = f'Falha após {self.max_search_attempts} tentativas de busca'
                    return result

        return result

    def _execute_search_actions(self, mapped_data: Dict) -> Dict:
        """
        Executa ações específicas para busca.

        Args:
            mapped_data (dict): Dados mapeados

        Returns:
            dict: Resultado das ações de busca
        """
        result = {
            'actions_executed': [],
            'current_values': {},
            'errors': []
        }

        # Usa ações de busca específicas ou ações padrão
        actions_to_execute = self.search_actions if self.search_actions else self.actions

        for action_config in actions_to_execute:
            try:
                # Para ações de busca, podemos capturar valores atuais
                action_result = self._execute_action(action_config, mapped_data)
                result['actions_executed'].append({
                    'action': action_config.get('type'),
                    'field': action_config.get('field'),
                    'success': True,
                    'result': action_result
                })

                # Se a ação retornou um valor, armazena como valor atual
                if action_result and isinstance(action_result, dict) and 'value' in action_result:
                    field = action_config.get('field')
                    if field:
                        result['current_values'][field] = action_result['value']

            except Exception as e:
                result['errors'].append({
                    'action': action_config.get('type'),
                    'field': action_config.get('field'),
                    'error': str(e)
                })

                # Se a ação é obrigatória para busca, interrompe
                if action_config.get('required', False):
                    raise

        return result

    def _detect_changes_needed(self, new_data: Dict, current_values: Dict) -> List[str]:
        """
        Detecta se há alterações necessárias entre dados novos e atuais.

        Args:
            new_data (dict): Novos dados
            current_values (dict): Valores atuais

        Returns:
            list: Lista de campos que precisam ser atualizados
        """
        changes_needed = []

        # Verifica cada campo que pode ser atualizado
        update_fields = self.config.get('update_fields', [])
        if not update_fields:
            # Se não especificado, usa todos os campos mapeados
            update_fields = list(new_data.keys())

        for field in update_fields:
            if field in new_data and field in current_values:
                new_value = str(new_data[field]).strip()
                current_value = str(current_values[field]).strip()

                if new_value != current_value:
                    changes_needed.append(field)
                    self.logger.debug(f"Campo '{field}' precisa ser atualizado: '{current_value}' → '{new_value}'")
            elif field in new_data:
                # Campo existe nos novos dados mas não nos atuais
                changes_needed.append(field)
                self.logger.debug(f"Campo '{field}' será adicionado")

        return changes_needed

    def _execute_update_actions(self, mapped_data: Dict) -> Dict:
        """
        Executa ações específicas para atualização.

        Args:
            mapped_data (dict): Dados mapeados

        Returns:
            dict: Resultado das ações de atualização
        """
        result = {
            'actions_executed': [],
            'success': True,
            'errors': []
        }

        # Usa ações de atualização específicas ou ações padrão
        actions_to_execute = self.update_actions if self.update_actions else self.actions

        for action_config in actions_to_execute:
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

                # Se a ação é obrigatória, interrompe o processamento
                if action_config.get('required', False):
                    raise

        return result

    def _execute_action(self, action_config: Dict, mapped_data: Dict) -> Any:
        """
        Executa uma ação específica.

        Args:
            action_config (dict): Configuração da ação
            mapped_data (dict): Dados mapeados

        Returns:
            any: Resultado da execução da ação
        """
        action_type = action_config.get('type')
        field = action_config.get('field')

        if not action_type:
            raise ValueError("Configuração de ação sem tipo")

        if not field:
            raise ValueError("Configuração de ação sem campo")

        # Obtém valor do campo
        value = self._get_action_value(action_config, mapped_data)

        # Cria e executa a ação
        action = ActionFactory.create_action(action_type, action_config)
        return action.execute(field, value)

    def _get_action_value(self, action_config: Dict, mapped_data: Dict):
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

        # Para ações que não precisam de valor
        if action_config.get('type') in ['click', 'wait', 'screenshot']:
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
                self.logger.warning(f"Campo de origem '{source_field}' não encontrado no registro")

        return mapped_data

    def _generate_update_report(self):
        """Gera relatório final da atualização."""
        successful = len([r for r in self.results if r.get('success')])
        updated = len([r for r in self.results if r.get('updated')])
        searched = len([r for r in self.results if r.get('search_successful')])

        self.logger.info("📊 Relatório de Atualização:")
        self.logger.info(f"   Total de registros: {len(self.results)}")
        self.logger.info(f"   Buscas bem-sucedidas: {searched}")
        self.logger.info(f"   Registros atualizados: {updated}")
        self.logger.info(f"   Registros sem alteração: {successful - updated}")
        self.logger.info(f"   Taxa de sucesso: {(successful / len(self.results)) * 100 if self.results else 0:.1f}%")

    def get_summary(self) -> Dict:
        """
        Retorna um resumo da execução da atualização.

        Returns:
            dict: Resumo com estatísticas da execução
        """
        successful = len([r for r in self.results if r.get('success')])
        updated = len([r for r in self.results if r.get('updated')])
        searched = len([r for r in self.results if r.get('search_successful')])

        total_search_actions = 0
        total_update_actions = 0
        successful_search_actions = 0
        successful_update_actions = 0

        for result in self.results:
            total_search_actions += len(result.get('search_actions', []))
            total_update_actions += len(result.get('update_actions', []))

            if result.get('search_successful'):
                successful_search_actions += len(result.get('search_actions', []))

            if result.get('success') and result.get('updated'):
                successful_update_actions += len(result.get('update_actions', []))

        return {
            'total_records': len(self.results),
            'successful_records': successful,
            'updated_records': updated,
            'searched_successfully': searched,
            'total_search_actions': total_search_actions,
            'successful_search_actions': successful_search_actions,
            'total_update_actions': total_update_actions,
            'successful_update_actions': successful_update_actions,
            'update_rate': (updated / len(self.results)) * 100 if self.results else 0,
            'search_success_rate': (searched / len(self.results)) * 100 if self.results else 0
        }
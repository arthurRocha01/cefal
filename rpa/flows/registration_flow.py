"""Fluxo especializado para operações de cadastro no CeFal.

Este fluxo otimiza operações de cadastro com validação de dados,
confirmação de sucesso e tratamento específico de erros de registro.
"""

from typing import Dict, List, Any
from rpa.flows.base_flow import BaseFlow
from rpa.actions.action_factory import ActionFactory
from utils.logging import get_logger


class RegistrationFlow(BaseFlow):
    """Fluxo especializado para operações de cadastro."""

    def __init__(self, workflow_config: Dict, data: List[Dict]):
        """
        Inicializa o fluxo de cadastro.

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

        # Configurações específicas para cadastro
        self.require_confirmation = workflow_config.get('require_confirmation', True)
        self.max_retries = workflow_config.get('max_retries', 3)
        self.confirmation_actions = workflow_config.get('confirmation_actions', [])

    def execute(self) -> List[Dict]:
        """
        Executa o fluxo de cadastro completo.

        Returns:
            list: Lista de resultados para cada registro processado
        """
        workflow_desc = self.config.get('description', 'Cadastro')
        self.logger.info(f"Iniciando fluxo de cadastro: {workflow_desc}")
        self.logger.info(f"Total de registros: {len(self.data)}")

        # 1. Executa passos iniciais
        self.execute_initial_steps()

        # 2. Processa cada registro de dados
        for record_idx, record in enumerate(self.data):
            self.logger.info(f"Processando registro {record_idx + 1}/{len(self.data)}")

            try:
                result = self._process_registration_record(record, record_idx)
                self.results.append(result)

                if result['success']:
                    self.logger.info(f"✅ Registro {record_idx + 1} cadastrado com sucesso")
                else:
                    self.logger.warning(f"⚠️ Registro {record_idx + 1} falhou: {result.get('error', 'Erro desconhecido')}")

            except Exception as e:
                self.logger.error(f"❌ Erro crítico ao processar registro {record_idx + 1}", error=str(e))
                self.results.append({
                    'record_index': record_idx,
                    'success': False,
                    'error': str(e),
                    'record': record,
                    'retry_count': 0
                })

        # 3. Gera relatório final
        self._generate_registration_report()

        return self.results

    def _process_registration_record(self, record: Dict, record_idx: int) -> Dict:
        """
        Processa um registro para cadastro com validação e confirmação.

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
            'actions_executed': [],
            'confirmation_actions': [],
            'validation_errors': [],
            'retry_count': 0,
            'errors': []
        }

        # 1. Valida dados do registro
        validation_result = self._validate_registration_data(record)
        if not validation_result['valid']:
            result['success'] = False
            result['validation_errors'] = validation_result['errors']
            result['error'] = 'Dados inválidos para cadastro'
            return result

        # 2. Mapeia dados do registro
        mapped_data = self._map_record_data(record)

        # 3. Executa ações de cadastro com retry
        for retry in range(self.max_retries):
            try:
                registration_result = self._execute_registration_actions(mapped_data)
                result['actions_executed'] = registration_result['actions_executed']
                result['retry_count'] = retry

                # 4. Confirma cadastro se necessário
                if self.require_confirmation:
                    confirmation_result = self._confirm_registration(mapped_data)
                    result['confirmation_actions'] = confirmation_result['actions_executed']

                    if not confirmation_result['success']:
                        result['success'] = False
                        result['error'] = 'Falha na confirmação do cadastro'
                        result['errors'].extend(confirmation_result['errors'])
                        continue  # Tenta novamente

                # Cadastro bem-sucedido
                return result

            except Exception as e:
                self.logger.warning(f"Tentativa {retry + 1}/{self.max_retries} falhou", error=str(e))
                result['errors'].append({
                    'retry': retry + 1,
                    'error': str(e)
                })

                if retry == self.max_retries - 1:
                    result['success'] = False
                    result['error'] = f'Falha após {self.max_retries} tentativas'
                    return result

        return result

    def _validate_registration_data(self, record: Dict) -> Dict:
        """
        Valida dados para cadastro.

        Args:
            record (dict): Dados do registro

        Returns:
            dict: Resultado da validação
        """
        errors = []

        # Verifica campos obrigatórios
        required_fields = self.config.get('required_fields', [])
        for field in required_fields:
            if field not in record or not record[field]:
                errors.append(f'Campo obrigatório "{field}" ausente ou vazio')

        # Validações específicas por tipo de campo
        field_validations = self.config.get('field_validations', {})
        for field, validation in field_validations.items():
            if field in record:
                value = record[field]

                if validation.get('required') and not value:
                    errors.append(f'Campo "{field}" é obrigatório')

                if validation.get('min_length') and len(str(value)) < validation['min_length']:
                    errors.append(f'Campo "{field}" deve ter pelo menos {validation["min_length"]} caracteres')

                if validation.get('max_length') and len(str(value)) > validation['max_length']:
                    errors.append(f'Campo "{field}" deve ter no máximo {validation["max_length"]} caracteres')

                if validation.get('pattern'):
                    import re
                    if not re.match(validation['pattern'], str(value)):
                        errors.append(f'Campo "{field}" não corresponde ao padrão esperado')

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

    def _execute_registration_actions(self, mapped_data: Dict) -> Dict:
        """
        Executa ações específicas para cadastro.

        Args:
            mapped_data (dict): Dados mapeados

        Returns:
            dict: Resultado das ações
        """
        result = {
            'actions_executed': [],
            'errors': []
        }

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
                result['errors'].append({
                    'action': action_config.get('type'),
                    'field': action_config.get('field'),
                    'error': str(e)
                })

                # Se a ação é obrigatória, interrompe o processamento
                if action_config.get('required', False):
                    raise

        return result

    def _confirm_registration(self, mapped_data: Dict) -> Dict:
        """
        Confirma que o cadastro foi realizado com sucesso.

        Args:
            mapped_data (dict): Dados mapeados

        Returns:
            dict: Resultado da confirmação
        """
        result = {
            'actions_executed': [],
            'success': True,
            'errors': []
        }

        for action_config in self.confirmation_actions:
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

    def _generate_registration_report(self):
        """Gera relatório final do cadastro."""
        successful = len([r for r in self.results if r.get('success')])
        failed = len(self.results) - successful

        total_retries = sum(r.get('retry_count', 0) for r in self.results)
        avg_retries = total_retries / len(self.results) if self.results else 0

        self.logger.info("📊 Relatório de Cadastro:")
        self.logger.info(f"   Total de registros: {len(self.results)}")
        self.logger.info(f"   Cadastros bem-sucedidos: {successful}")
        self.logger.info(f"   Cadastros com falha: {failed}")
        self.logger.info(f"   Taxa de sucesso: {(successful / len(self.results)) * 100 if self.results else 0:.1f}%")
        self.logger.info(f"   Tentativas médias por registro: {avg_retries:.1f}")

    def get_summary(self) -> Dict:
        """
        Retorna um resumo da execução do cadastro.

        Returns:
            dict: Resumo com estatísticas da execução
        """
        successful = len([r for r in self.results if r.get('success')])
        failed = len(self.results) - successful

        total_actions = 0
        successful_actions = 0
        total_retries = 0

        for result in self.results:
            total_retries += result.get('retry_count', 0)
            if result.get('success'):
                successful_actions += len(result.get('actions_executed', []))
                successful_actions += len(result.get('confirmation_actions', []))
            total_actions += len(result.get('actions_executed', [])) + len(result.get('confirmation_actions', [])) + len(result.get('errors', []))

        return {
            'total_records': len(self.results),
            'successful_records': successful,
            'failed_records': failed,
            'total_actions': total_actions,
            'successful_actions': successful_actions,
            'total_retries': total_retries,
            'avg_retries_per_record': total_retries / len(self.results) if self.results else 0,
            'success_rate': (successful / len(self.results)) * 100 if self.results else 0
        }
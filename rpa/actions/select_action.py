"""Implementação da ação de seleção (select) para o CeFal."""

from rpa.actions.base_action import BaseAction
from typing import Optional
from rpa.infra.botcity import find, click, type_text
from time import sleep


class SelectAction(BaseAction):
    """Ação para realizar seleção em dropdowns/comboboxes."""

    def execute(self, field: str, value: Optional[str] = None) -> bool:
        """
        Executa ação de seleção no campo especificado.

        Args:
            field (str): Nome do campo/alvo da ação
            value (str, optional): Valor a ser selecionado no dropdown

        Returns:
            bool: True se a seleção foi executada com sucesso

        Raises:
            Exception: Se não conseguir encontrar o campo ou selecionar o valor
        """
        try:
            # Registra início da execução
            self._log_execution_start(field, value)

            # Obtém tempo de espera da configuração ou usa padrão
            time_wait = self.config.get('time_wait', 0.3)

            # Verifica se há valor para selecionar
            if not value:
                raise ValueError(f"Valor não fornecido para seleção no campo: {field}")

            # Encontra e clica no dropdown para abri-lo
            if not find(field):
                raise Exception(f'Dropdown não encontrado: {field}')

            click()
            sleep(time_wait)

            # Digita o valor para selecionar
            type_text(value)
            sleep(time_wait)

            # Pressiona Enter para confirmar a seleção
            type_text("{ENTER}")

            # Registra sucesso
            self._log_execution_success(field, value)
            return True

        except Exception as e:
            self._log_execution_error(field, e, value)
            raise
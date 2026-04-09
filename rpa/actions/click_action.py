"""Implementação da ação de click para o CeFal."""

from rpa.actions.base_action import BaseAction
from typing import Optional
from rpa.infra.botcity import find, click


class ClickAction(BaseAction):
    """Ação para realizar clicks em elementos da interface."""

    def execute(self, field: str, value: Optional[str] = None) -> bool:
        """
        Executa ação de click no campo especificado.

        Args:
            field (str): Nome do campo/alvo da ação
            value (str, optional): Valor não utilizado para click

        Returns:
            bool: True se o click foi executado com sucesso

        Raises:
            Exception: Se não conseguir encontrar a imagem ou clicar
        """
        try:
            # Registra início da execução
            self._log_execution_start(field, value)

            # Obtém tempo de espera da configuração ou usa padrão
            time_wait = self.config.get('time_wait', 0.3)

            # Encontra e clica na imagem
            if not find(field):
                raise Exception(f'Imagem não encontrada: {field}')

            click()

            # Registra sucesso
            self._log_execution_success(field, value)
            return True

        except Exception as e:
            self._log_execution_error(field, e, value)
            raise
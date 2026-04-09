"""Implementação da ação de digitação para o CeFal."""

from rpa.actions.base_action import BaseAction
from typing import Optional
from rpa.actions.click import click_image
from rpa.infra.botcity import type_text


class TypeAction(BaseAction):
    """Ação para realizar digitação em elementos da interface."""

    def execute(self, field: str, value: Optional[str] = None) -> bool:
        """
        Executa ação de digitação no campo especificado.

        Args:
            field (str): Nome do campo/alvo da ação
            value (str, optional): Texto a ser digitado

        Returns:
            bool: True se a digitação foi executada com sucesso

        Raises:
            Exception: Se não conseguir encontrar a imagem ou digitar
        """
        try:
            # Registra início da execução
            self._log_execution_start(field, value)

            # Obtém tempo de espera da configuração ou usa padrão
            time_wait = self.config.get('time_wait', 0.3)

            # Primeiro clica no campo
            click_image(field, time_wait)

            # Depois digita o texto
            if value:
                type_text(value)

            # Simula sucesso
            success = True

            if success:
                self._log_execution_success(field, value)
                return True
            else:
                raise Exception(f"Failed to type in field: {field}")

        except Exception as e:
            self._log_execution_error(field, e, value)
            raise
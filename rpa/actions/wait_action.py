"""Implementação da ação de espera (wait) para o CeFal."""

from rpa.actions.base_action import BaseAction
from typing import Optional
import time


class WaitAction(BaseAction):
    """Ação para realizar pausas/esperas durante a execução."""

    def execute(self, field: str, value: Optional[str] = None) -> bool:
        """
        Executa ação de espera pelo tempo especificado.

        Args:
            field (str): Nome do campo/alvo da ação (não usado para wait)
            value (str, optional): Tempo de espera em segundos (string convertida para float)

        Returns:
            bool: True se a espera foi executada com sucesso

        Raises:
            Exception: Se o valor não for um número válido
        """
        try:
            # Registra início da execução
            self._log_execution_start(field, value)

            # Converte valor para segundos (float)
            wait_time = float(value) if value else 1.0

            # Realiza a espera
            time.sleep(wait_time)

            # Log de sucesso
            self._log_execution_success(field, value)
            return True

        except ValueError as e:
            error_msg = f"Tempo de espera inválido: '{value}'. Deve ser um número."
            self._log_execution_error(field, Exception(error_msg), value)
            raise Exception(error_msg) from e
        except Exception as e:
            self._log_execution_error(field, e, value)
            raise
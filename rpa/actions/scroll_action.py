"""Implementação da ação de rolagem (scroll) para o CeFal."""

from rpa.actions.base_action import BaseAction
from typing import Optional
from rpa.infra.botcity import scroll


class ScrollAction(BaseAction):
    """Ação para realizar rolagem na interface."""

    def execute(self, field: str, value: Optional[str] = None) -> bool:
        """
        Executa ação de rolagem.

        Args:
            field (str): Direção da rolagem (up/down/left/right)
            value (str, optional): Quantidade de rolagem (em pixels ou passos)

        Returns:
            bool: True se a rolagem foi executada com sucesso

        Raises:
            Exception: Se a direção for inválida ou ocorrer erro na rolagem
        """
        try:
            # Registra início da execução
            self._log_execution_start(field, value)

            # Valida direção (atualmente só up/down são suportados)
            valid_directions = ['up', 'down']
            if field not in valid_directions:
                raise ValueError(f"Direção de rolagem inválida: '{field}'. Use: {valid_directions}")

            # Converte valor para inteiro ou usa padrão
            amount = int(value) if value else 100

            # Executa a rolagem
            scroll(field, amount)

            # Registra sucesso
            self._log_execution_success(field, value)
            return True

        except ValueError as e:
            # Verifica se o erro é da direção inválida ou do valor
            if field not in ['up', 'down']:
                # Erro de direção inválida - re-levanta a exceção original
                self._log_execution_error(field, e, value)
                raise
            else:
                # Erro de valor inválido
                error_msg = f"Valor de rolagem inválido: '{value}'. Deve ser um número inteiro."
                self._log_execution_error(field, Exception(error_msg), value)
                raise Exception(error_msg) from e
        except Exception as e:
            self._log_execution_error(field, e, value)
            raise
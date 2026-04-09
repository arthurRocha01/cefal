"""Implementação da ação de captura de tela (screenshot) para o CeFal."""

from rpa.actions.base_action import BaseAction
from typing import Optional
import os
import datetime
from rpa.infra.botcity import take_screenshot


class ScreenshotAction(BaseAction):
    """Ação para realizar capturas de tela durante a execução."""

    def execute(self, field: str, value: Optional[str] = None) -> bool:
        """
        Executa ação de captura de tela.

        Args:
            field (str): Nome/identificador da captura
            value (str, optional): Caminho para salvar a captura (opcional)

        Returns:
            bool: True se a captura foi executada com sucesso

        Raises:
            Exception: Se não conseguir realizar a captura
        """
        try:
            # Registra início da execução
            self._log_execution_start(field, value)

            # Determina caminho para salvar
            if value:
                save_path = value
            else:
                # Cria diretório screenshots se não existir
                screenshots_dir = "screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)

                # Gera nome de arquivo com timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{field}_{timestamp}.png"
                save_path = os.path.join(screenshots_dir, filename)

            # Tira a captura de tela
            take_screenshot(save_path)

            # Registra sucesso
            self._log_execution_success(field, value)
            return True

        except Exception as e:
            self._log_execution_error(field, e, value)
            raise
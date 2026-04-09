"""Sistema de logging estruturado para o CeFal."""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional


class CeFalLogger:
    """Logger estruturado para workflows do CeFal."""

    def __init__(self, workflow_name: str, log_dir: str = "logs"):
        """
        Inicializa o logger para um workflow específico.

        Args:
            workflow_name (str): Nome do workflow
            log_dir (str): Diretório para armazenar logs
        """
        self.workflow_name = workflow_name
        self.log_dir = log_dir

        # Cria diretório de logs se não existir
        os.makedirs(log_dir, exist_ok=True)

        # Configura logger
        self.logger = logging.getLogger(f"cefal.{workflow_name}")
        self.logger.setLevel(logging.DEBUG)

        # Remove handlers existentes para evitar duplicação
        self.logger.handlers.clear()

        # Formato dos logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para arquivo
        log_file = os.path.join(log_dir, f"{workflow_name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Adiciona handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str, action: Optional[str] = None, field: Optional[str] = None):
        """
        Log de nível INFO.

        Args:
            message (str): Mensagem do log
            action (str, optional): Tipo de ação executada
            field (str, optional): Campo/alvo da ação
        """
        structured_msg = self._structure_message(message, action, field)
        self.logger.info(structured_msg)

    def error(self, message: str, action: Optional[str] = None, field: Optional[str] = None,
              error: Optional[Exception] = None):
        """
        Log de nível ERROR.

        Args:
            message (str): Mensagem do log
            action (str, optional): Tipo de ação executada
            field (str, optional): Campo/alvo da ação
            error (Exception, optional): Exceção capturada
        """
        structured_msg = self._structure_message(message, action, field)
        if error:
            structured_msg += f" | Error: {type(error).__name__}: {str(error)}"
        self.logger.error(structured_msg)

    def debug(self, message: str, action: Optional[str] = None, field: Optional[str] = None):
        """
        Log de nível DEBUG.

        Args:
            message (str): Mensagem do log
            action (str, optional): Tipo de ação executada
            field (str, optional): Campo/alvo da ação
        """
        structured_msg = self._structure_message(message, action, field)
        self.logger.debug(structured_msg)

    def warning(self, message: str, action: Optional[str] = None, field: Optional[str] = None):
        """
        Log de nível WARNING.

        Args:
            message (str): Mensagem do log
            action (str, optional): Tipo de ação executada
            field (str, optional): Campo/alvo da ação
        """
        structured_msg = self._structure_message(message, action, field)
        self.logger.warning(structured_msg)

    def _structure_message(self, message: str, action: Optional[str] = None, field: Optional[str] = None) -> str:
        """
        Estrutura a mensagem de log com metadados.

        Args:
            message (str): Mensagem base
            action (str, optional): Tipo de ação
            field (str, optional): Campo/alvo

        Returns:
            str: Mensagem estruturada
        """
        parts = []
        if action:
            parts.append(f"Action: {action}")
        if field:
            parts.append(f"Field: {field}")

        if parts:
            return f"{message} | {' | '.join(parts)}"
        return message

    def start_workflow(self, config: dict = None):
        """Log de início de workflow."""
        config_info = f" | Config: {config}" if config else ""
        self.info(f"Starting workflow '{self.workflow_name}'{config_info}")

    def end_workflow(self, success: bool = True, duration: float = None):
        """Log de término de workflow."""
        status = "SUCCESS" if success else "FAILED"
        duration_info = f" | Duration: {duration:.2f}s" if duration is not None else ""
        self.info(f"Workflow '{self.workflow_name}' completed with status: {status}{duration_info}")


# Função auxiliar para criar logger rapidamente
def get_logger(workflow_name: str, log_dir: str = "logs") -> CeFalLogger:
    """
    Cria e retorna um logger para o workflow especificado.

    Args:
        workflow_name (str): Nome do workflow
        log_dir (str): Diretório para armazenar logs

    Returns:
        CeFalLogger: Instância do logger
    """
    return CeFalLogger(workflow_name, log_dir)
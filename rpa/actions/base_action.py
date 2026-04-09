"""Classe base abstrata para todas as ações do CeFal."""
from abc import ABC, abstractmethod
from typing import Optional


class BaseAction(ABC):
    """Classe base abstrata para implementação de ações de automação."""

    def __init__(self, config=None, logger=None):
        """
        Inicializa a ação com configuração.

        Args:
            config (dict, optional): Configuração específica da ação
            logger: Logger para registrar execução da ação
        """
        self.config = config or {}
        self.logger = logger

    @abstractmethod
    def execute(self, field, value=None):
        """
        Executa a ação no campo especificado.

        Args:
            field (str): Nome do campo/alvo da ação
            value (any, optional): Valor a ser usado na ação

        Returns:
            bool: True se a ação foi executada com sucesso
        """
        pass

    def _log_execution_start(self, field: str, value: Optional[str] = None):
        """Registra início da execução da ação."""
        if self.logger:
            action_type = self.__class__.__name__.replace('Action', '').lower()
            self.logger.info(
                f"Executing {action_type} action",
                action=action_type,
                field=field
            )

    def _log_execution_success(self, field: str, value: Optional[str] = None):
        """Registra sucesso na execução da ação."""
        if self.logger:
            action_type = self.__class__.__name__.replace('Action', '').lower()
            self.logger.info(
                f"{action_type.capitalize()} action completed successfully",
                action=action_type,
                field=field
            )

    def _log_execution_error(self, field: str, error: Exception, value: Optional[str] = None):
        """Registra erro na execução da ação."""
        if self.logger:
            action_type = self.__class__.__name__.replace('Action', '').lower()
            self.logger.error(
                f"{action_type.capitalize()} action failed",
                action=action_type,
                field=field,
                error=error
            )

    def validate(self, field, value=None):
        """
        Valida se a ação pode ser executada.

        Args:
            field (str): Nome do campo/alvo da ação
            value (any, optional): Valor a ser usado na ação

        Returns:
            bool: True se a ação pode ser executada

        Raises:
            ValueError: Se validação falhar
        """
        required = self.config.get('required', False)
        if required and not value:
            raise ValueError(f"Campo '{field}' é obrigatório")
        return True

    def get_description(self):
        """Retorna descrição da ação para logs."""
        action_type = self.__class__.__name__.replace('Action', '').lower()
        return f"{action_type} action"

    def __str__(self):
        """Representação em string da ação."""
        return f"{self.__class__.__name__}(config={self.config})"
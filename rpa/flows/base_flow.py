"""Classe base abstrata para todos os fluxos do CeFal."""
from abc import ABC, abstractmethod


class BaseFlow(ABC):
    """Classe base abstrata para implementação de fluxos de automação."""

    def __init__(self, workflow_config, data):
        """
        Inicializa o fluxo com configuração e dados.

        Args:
            workflow_config (dict): Configuração do workflow
            data (list): Lista de dicionários com dados a serem processados
        """
        self.config = workflow_config
        self.data = data
        self.template = workflow_config.get('template', 'default')

    @abstractmethod
    def execute(self):
        """Método principal de execução do fluxo."""
        pass

    def get_steps(self):
        """Retorna passos iniciais do workflow."""
        return self.config.get('steps', [])

    def get_actions(self):
        """Retorna ações do workflow."""
        return self.config.get('actions', [])

    def execute_initial_steps(self):
        """Executa passos iniciais do workflow."""
        from rpa.flows.take_initial_steps import take_initial_steps
        take_initial_steps(self.template, self.get_steps())
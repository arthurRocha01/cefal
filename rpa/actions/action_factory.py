"""Factory para criação de ações do CeFal."""


class ActionFactory:
    """Factory para criar instâncias de ações baseadas em tipo."""

    _action_types = {
        # Tipos básicos serão registrados quando implementados
    }

    @classmethod
    def create_action(cls, action_type, config=None, logger=None):
        """
        Cria uma instância da ação especificada.

        Args:
            action_type (str): Tipo da ação (ex: 'click', 'type')
            config (dict, optional): Configuração específica da ação
            logger: Logger para registrar execução da ação

        Returns:
            BaseAction: Instância da ação criada

        Raises:
            ValueError: Se o tipo de ação não for suportado
        """
        action_class = cls._action_types.get(action_type)
        if not action_class:
            raise ValueError(f"Tipo de ação não suportado: {action_type}")
        return action_class(config, logger)

    @classmethod
    def register_action(cls, action_type, action_class):
        """
        Registra um novo tipo de ação na factory.

        Args:
            action_type (str): Tipo da ação (ex: 'click', 'type')
            action_class (class): Classe da ação (deve herdar de BaseAction)

        Raises:
            TypeError: Se a classe não herdar de BaseAction
        """
        from rpa.actions.base_action import BaseAction

        if not issubclass(action_class, BaseAction):
            raise TypeError(f"A classe {action_class.__name__} deve herdar de BaseAction")

        cls._action_types[action_type] = action_class

    @classmethod
    def get_registered_actions(cls):
        """
        Retorna lista de tipos de ação registrados.

        Returns:
            list: Lista de strings com tipos de ação registrados
        """
        return list(cls._action_types.keys())

    @classmethod
    def is_action_supported(cls, action_type):
        """
        Verifica se um tipo de ação é suportado.

        Args:
            action_type (str): Tipo da ação

        Returns:
            bool: True se o tipo de ação é suportado
        """
        return action_type in cls._action_types

    @classmethod
    def clear_registry(cls):
        """Limpa o registro de tipos de ação (útil para testes)."""
        cls._action_types.clear()

    @classmethod
    def initialize(cls):
        """
        Inicializa a factory registrando todas as ações disponíveis.
        Deve ser chamado uma vez no início da aplicação.
        """
        # Importa as classes de ação
        from rpa.actions.click_action import ClickAction
        from rpa.actions.type_action import TypeAction
        from rpa.actions.wait_action import WaitAction
        from rpa.actions.select_action import SelectAction
        from rpa.actions.scroll_action import ScrollAction
        from rpa.actions.screenshot_action import ScreenshotAction

        # Registra as ações
        cls.register_action('click', ClickAction)
        cls.register_action('type', TypeAction)
        cls.register_action('wait', WaitAction)
        cls.register_action('select', SelectAction)
        cls.register_action('scroll', ScrollAction)
        cls.register_action('screenshot', ScreenshotAction)
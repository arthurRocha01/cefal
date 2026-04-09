"""Testes para a factory de ações."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

import pytest
from unittest.mock import Mock
from rpa.actions.base_action import BaseAction


def test_action_factory_initial_state():
    """Testa estado inicial da ActionFactory."""
    from rpa.actions.action_factory import ActionFactory

    # Limpa registry para teste (já que __init__.py registra ações automaticamente)
    ActionFactory.clear_registry()

    # Factory deve começar sem ações registradas após limpeza
    assert ActionFactory.get_registered_actions() == []


def test_action_factory_register_action():
    """Testa registro de ações na factory."""
    from rpa.actions.action_factory import ActionFactory

    # Cria uma ação de teste
    class TestAction(BaseAction):
        def execute(self, field, value=None):
            return True

    # Registra a ação
    ActionFactory.register_action('test', TestAction)

    # Verifica se foi registrada
    assert 'test' in ActionFactory.get_registered_actions()
    assert ActionFactory.is_action_supported('test') is True


def test_action_factory_register_invalid_action():
    """Testa registro de ação inválida."""
    from rpa.actions.action_factory import ActionFactory

    # Classe que não herda de BaseAction
    class InvalidAction:
        pass

    # Tenta registrar ação inválida
    with pytest.raises(TypeError, match="deve herdar de BaseAction"):
        ActionFactory.register_action('invalid', InvalidAction)


def test_action_factory_create_action():
    """Testa criação de ações pela factory."""
    from rpa.actions.action_factory import ActionFactory

    # Cria e registra uma ação de teste
    class TestAction(BaseAction):
        def execute(self, field, value=None):
            return field == 'test_field'

    ActionFactory.register_action('test', TestAction)

    # Cria ação sem config
    action1 = ActionFactory.create_action('test')
    assert isinstance(action1, TestAction)
    assert action1.config == {}
    assert action1.logger is None
    assert action1.execute('test_field') is True

    # Cria ação com config
    config = {'required': True, 'timeout': 5}
    action2 = ActionFactory.create_action('test', config)
    assert action2.config == config
    assert action2.logger is None

    # Cria ação com logger
    mock_logger = Mock()
    action3 = ActionFactory.create_action('test', config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


def test_action_factory_create_unsupported_action():
    """Testa criação de ação não suportada."""
    from rpa.actions.action_factory import ActionFactory

    # Tenta criar ação não registrada
    with pytest.raises(ValueError, match="Tipo de ação não suportado: nonexistent"):
        ActionFactory.create_action('nonexistent')


def test_action_factory_clear_registry():
    """Testa limpeza do registro de ações."""
    from rpa.actions.action_factory import ActionFactory

    # Limpa registro para começar limpo
    ActionFactory.clear_registry()

    # Registra algumas ações
    class Action1(BaseAction):
        def execute(self, field, value=None):
            return True

    class Action2(BaseAction):
        def execute(self, field, value=None):
            return True

    ActionFactory.register_action('action1', Action1)
    ActionFactory.register_action('action2', Action2)

    # Verifica que estão registradas
    assert len(ActionFactory.get_registered_actions()) == 2

    # Limpa o registro
    ActionFactory.clear_registry()

    # Verifica que está vazio
    assert ActionFactory.get_registered_actions() == []


def test_action_factory_is_action_supported():
    """Testa verificação de suporte a tipo de ação."""
    from rpa.actions.action_factory import ActionFactory

    # Ação não registrada não é suportada
    assert ActionFactory.is_action_supported('nonexistent') is False

    # Registra uma ação
    class TestAction(BaseAction):
        def execute(self, field, value=None):
            return True

    ActionFactory.register_action('supported', TestAction)

    # Agora é suportada
    assert ActionFactory.is_action_supported('supported') is True


def test_action_factory_get_registered_actions():
    """Testa obtenção de lista de ações registradas."""
    from rpa.actions.action_factory import ActionFactory

    # Limpa registro para teste limpo
    ActionFactory.clear_registry()

    # Registra múltiplas ações
    class ActionA(BaseAction):
        def execute(self, field, value=None):
            return True

    class ActionB(BaseAction):
        def execute(self, field, value=None):
            return True

    ActionFactory.register_action('action_a', ActionA)
    ActionFactory.register_action('action_b', ActionB)

    # Verifica lista de ações registradas
    registered = ActionFactory.get_registered_actions()
    assert len(registered) == 2
    assert 'action_a' in registered
    assert 'action_b' in registered
    assert sorted(registered) == ['action_a', 'action_b']


if __name__ == '__main__':
    # Executa todos os testes
    test_action_factory_initial_state()
    test_action_factory_register_action()
    test_action_factory_register_invalid_action()
    test_action_factory_create_action()
    test_action_factory_create_unsupported_action()
    test_action_factory_clear_registry()
    test_action_factory_is_action_supported()
    test_action_factory_get_registered_actions()
    print("✓ Todos os testes de ActionFactory passaram!")
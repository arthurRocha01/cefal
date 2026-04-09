"""Testes para a classe base de ações."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

import pytest
from unittest.mock import Mock, patch
from abc import ABC


def test_base_action_is_abstract():
    """Testa se BaseAction é uma classe abstrata."""
    from rpa.actions.base_action import BaseAction

    # Verifica que BaseAction é uma classe abstrata
    assert issubclass(BaseAction, ABC)

    # Tenta instanciar diretamente (deve falhar)
    with pytest.raises(TypeError):
        BaseAction()


def test_base_action_abstract_methods():
    """Testa se BaseAction tem métodos abstratos obrigatórios."""
    from rpa.actions.base_action import BaseAction

    # Cria uma implementação concreta para teste
    class ConcreteAction(BaseAction):
        def execute(self, field, value=None):
            return True

    # Testa instanciação da classe concreta
    action = ConcreteAction()
    assert isinstance(action, BaseAction)
    assert action.execute('test') is True


def test_base_action_initialization():
    """Testa inicialização da BaseAction."""
    from rpa.actions.base_action import BaseAction

    class TestAction(BaseAction):
        def execute(self, field, value=None):
            return True

    # Testa inicialização sem config
    action1 = TestAction()
    assert action1.config == {}
    assert action1.logger is None

    # Testa inicialização com config
    config = {'required': True, 'timeout': 5}
    action2 = TestAction(config)
    assert action2.config == config
    assert action2.logger is None

    # Testa inicialização com logger
    mock_logger = Mock()
    action3 = TestAction(config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


def test_base_action_validate():
    """Testa método validate da BaseAction."""
    from rpa.actions.base_action import BaseAction

    class TestAction(BaseAction):
        def execute(self, field, value=None):
            return True

    # Testa validação sem required
    action = TestAction()
    assert action.validate('field', 'value') is True
    assert action.validate('field', None) is True
    assert action.validate('field', '') is True

    # Testa validação com required=True
    action_required = TestAction({'required': True})
    assert action_required.validate('field', 'value') is True
    assert action_required.validate('field', 'valid') is True

    # Testa validação com required=True e valor vazio
    with pytest.raises(ValueError, match="Campo 'field' é obrigatório"):
        action_required.validate('field', None)

    with pytest.raises(ValueError, match="Campo 'field' é obrigatório"):
        action_required.validate('field', '')


def test_base_action_get_description():
    """Testa método get_description da BaseAction."""
    from rpa.actions.base_action import BaseAction

    class ClickAction(BaseAction):
        def execute(self, field, value=None):
            return True

    class TypeAction(BaseAction):
        def execute(self, field, value=None):
            return True

    # Testa descrição para diferentes tipos de ação
    click_action = ClickAction()
    assert click_action.get_description() == "click action"

    type_action = TypeAction()
    assert type_action.get_description() == "type action"


def test_base_action_str_representation():
    """Testa representação em string da BaseAction."""
    from rpa.actions.base_action import BaseAction

    class TestAction(BaseAction):
        def execute(self, field, value=None):
            return True

    # Testa representação sem config
    action1 = TestAction()
    assert str(action1) == "TestAction(config={})"

    # Testa representação com config
    config = {'required': True}
    action2 = TestAction(config)
    assert str(action2) == "TestAction(config={'required': True})"


if __name__ == '__main__':
    # Executa todos os testes
    test_base_action_is_abstract()
    test_base_action_abstract_methods()
    test_base_action_initialization()
    test_base_action_validate()
    test_base_action_get_description()
    test_base_action_str_representation()
    print("✓ Todos os testes de BaseAction passaram!")
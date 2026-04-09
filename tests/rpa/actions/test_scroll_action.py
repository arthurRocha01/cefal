"""Testes para a ação de rolagem (ScrollAction)."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

import pytest
from unittest.mock import Mock, patch
from rpa.actions.base_action import BaseAction


def test_scroll_action_is_base_action_subclass():
    """Testa se ScrollAction herda de BaseAction."""
    from rpa.actions.scroll_action import ScrollAction

    assert issubclass(ScrollAction, BaseAction)


def test_scroll_action_initialization():
    """Testa inicialização da ScrollAction."""
    from rpa.actions.scroll_action import ScrollAction

    # Testa inicialização sem config
    action1 = ScrollAction()
    assert action1.config == {}
    assert action1.logger is None

    # Testa inicialização com config
    config = {'required': True, 'timeout': 5}
    action2 = ScrollAction(config)
    assert action2.config == config
    assert action2.logger is None

    # Testa inicialização com logger
    mock_logger = Mock()
    action3 = ScrollAction(config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


@patch('rpa.actions.scroll_action.scroll')
def test_scroll_action_execute_success(mock_scroll):
    """Testa execução bem-sucedida da ScrollAction."""
    from rpa.actions.scroll_action import ScrollAction

    action = ScrollAction()

    # Executa ação com direção válida
    result = action.execute('down', '200')
    assert result is True
    mock_scroll.assert_called_once_with('down', 200)


@patch('rpa.actions.scroll_action.scroll')
def test_scroll_action_execute_without_amount(mock_scroll):
    """Testa execução sem quantidade especificada (usa padrão)."""
    from rpa.actions.scroll_action import ScrollAction

    action = ScrollAction()

    # Executa ação sem valor (deve usar 100 como padrão)
    result = action.execute('up')
    assert result is True
    mock_scroll.assert_called_once_with('up', 100)


@patch('rpa.actions.scroll_action.scroll')
def test_scroll_action_execute_invalid_direction(mock_scroll):
    """Testa execução com direção inválida."""
    from rpa.actions.scroll_action import ScrollAction

    action = ScrollAction()

    # Deve levantar exceção para direção inválida
    with pytest.raises(Exception, match="Direção de rolagem inválida"):
        action.execute('invalid_direction', '100')

    # Não deve chamar scroll para direção inválida
    mock_scroll.assert_not_called()


@patch('rpa.actions.scroll_action.scroll')
def test_scroll_action_execute_invalid_amount(mock_scroll):
    """Testa execução com quantidade inválida."""
    from rpa.actions.scroll_action import ScrollAction

    action = ScrollAction()

    # Deve levantar exceção para valor não numérico
    with pytest.raises(Exception, match="Valor de rolagem inválido"):
        action.execute('down', 'invalid')

    # Não deve chamar scroll para valor inválido
    mock_scroll.assert_not_called()


@patch('rpa.actions.scroll_action.scroll')
def test_scroll_action_execute_with_logger(mock_scroll):
    """Testa execução com logger."""
    from rpa.actions.scroll_action import ScrollAction

    mock_logger = Mock()
    action = ScrollAction({'required': True}, mock_logger)

    # 'left' não é mais uma direção válida (só up/down)
    with pytest.raises(Exception, match="Direção de rolagem inválida"):
        action.execute('left', '150')

    # Não deve chamar scroll para direção inválida
    mock_scroll.assert_not_called()


def test_scroll_action_get_description():
    """Testa método get_description da ScrollAction."""
    from rpa.actions.scroll_action import ScrollAction

    action = ScrollAction()
    assert action.get_description() == "scroll action"


@patch('rpa.actions.scroll_action.scroll')
def test_scroll_action_execute_all_directions(mock_scroll):
    """Testa execução com todas as direções válidas."""
    from rpa.actions.scroll_action import ScrollAction

    action = ScrollAction()

    # Testa apenas direções válidas (up/down)
    for direction in ['up', 'down']:
        result = action.execute(direction, '100')
        assert result is True

    # Deve falhar para direções inválidas
    for direction in ['left', 'right']:
        with pytest.raises(Exception, match="Direção de rolagem inválida"):
            action.execute(direction, '100')


@patch('rpa.actions.scroll_action.scroll')
def test_scroll_action_execute_with_custom_config(mock_scroll):
    """Testa execução com configuração personalizada."""
    from rpa.actions.scroll_action import ScrollAction

    config = {'some_setting': 'value'}
    action = ScrollAction(config)

    result = action.execute('down', '300')
    assert result is True
    mock_scroll.assert_called_once_with('down', 300)


if __name__ == '__main__':
    # Executa todos os testes
    test_scroll_action_is_base_action_subclass()
    test_scroll_action_initialization()
    test_scroll_action_execute_success()
    test_scroll_action_execute_without_amount()
    test_scroll_action_execute_invalid_direction()
    test_scroll_action_execute_invalid_amount()
    test_scroll_action_execute_with_logger()
    test_scroll_action_get_description()
    test_scroll_action_execute_all_directions()
    test_scroll_action_execute_with_custom_config()
    print("✓ Todos os testes de ScrollAction passaram!")
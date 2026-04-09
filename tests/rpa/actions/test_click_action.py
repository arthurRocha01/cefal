"""Testes para a ação de click (ClickAction)."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

import pytest
from unittest.mock import Mock, patch
from rpa.actions.base_action import BaseAction


def test_click_action_is_base_action_subclass():
    """Testa se ClickAction herda de BaseAction."""
    from rpa.actions.click_action import ClickAction

    assert issubclass(ClickAction, BaseAction)


def test_click_action_initialization():
    """Testa inicialização da ClickAction."""
    from rpa.actions.click_action import ClickAction

    # Testa inicialização sem config
    action1 = ClickAction()
    assert action1.config == {}
    assert action1.logger is None

    # Testa inicialização com config
    config = {'required': True, 'timeout': 5}
    action2 = ClickAction(config)
    assert action2.config == config
    assert action2.logger is None

    # Testa inicialização com logger
    mock_logger = Mock()
    action3 = ClickAction(config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


@patch('rpa.actions.click_action.click')
@patch('rpa.actions.click_action.find')
def test_click_action_execute_success(mock_find, mock_click):
    """Testa execução bem-sucedida da ClickAction."""
    from rpa.actions.click_action import ClickAction

    action = ClickAction()
    mock_find.return_value = True  # Simula que encontrou a imagem

    # Executa ação
    result = action.execute('button_image')

    assert result is True
    mock_find.assert_called_once_with('button_image')
    mock_click.assert_called_once()


@patch('rpa.actions.click_action.click')
@patch('rpa.actions.click_action.find')
def test_click_action_execute_element_not_found(mock_find, mock_click):
    """Testa execução quando elemento não é encontrado."""
    from rpa.actions.click_action import ClickAction

    action = ClickAction()
    mock_find.return_value = False  # Simula que não encontrou a imagem

    # Deve levantar exceção
    with pytest.raises(Exception, match="Imagem não encontrada: button_image"):
        action.execute('button_image')

    mock_find.assert_called_once_with('button_image')
    mock_click.assert_not_called()


@patch('rpa.actions.click_action.click')
@patch('rpa.actions.click_action.find')
def test_click_action_execute_with_logger(mock_find, mock_click):
    """Testa execução com logger."""
    from rpa.actions.click_action import ClickAction

    mock_logger = Mock()
    action = ClickAction({'required': True}, mock_logger)
    mock_find.return_value = True

    result = action.execute('button_image')

    # Verifica que logger foi usado
    assert mock_logger.info.called
    assert result is True
    mock_find.assert_called_once_with('button_image')
    mock_click.assert_called_once()


def test_click_action_get_description():
    """Testa método get_description da ClickAction."""
    from rpa.actions.click_action import ClickAction

    action = ClickAction()
    assert action.get_description() == "click action"


@patch('rpa.actions.click_action.click')
@patch('rpa.actions.click_action.find')
def test_click_action_execute_with_custom_config(mock_find, mock_click):
    """Testa execução com configuração personalizada."""
    from rpa.actions.click_action import ClickAction

    config = {'some_setting': 'value'}
    action = ClickAction(config)
    mock_find.return_value = True

    result = action.execute('button_image')
    assert result is True
    mock_find.assert_called_once_with('button_image')
    mock_click.assert_called_once()


@patch('rpa.actions.click_action.click')
@patch('rpa.actions.click_action.find')
def test_click_action_execute_with_value_parameter(mock_find, mock_click):
    """Testa execução com parâmetro value (não utilizado)."""
    from rpa.actions.click_action import ClickAction

    action = ClickAction()
    mock_find.return_value = True

    # O parâmetro value é opcional e não utilizado
    result = action.execute('button_image', 'some_value')

    assert result is True
    mock_find.assert_called_once_with('button_image')
    mock_click.assert_called_once()


if __name__ == '__main__':
    # Executa todos os testes
    test_click_action_is_base_action_subclass()
    test_click_action_initialization()
    test_click_action_execute_success()
    test_click_action_execute_element_not_found()
    test_click_action_execute_with_logger()
    test_click_action_get_description()
    test_click_action_execute_with_custom_config()
    test_click_action_execute_with_value_parameter()
    print("✓ Todos os testes de ClickAction passaram!")
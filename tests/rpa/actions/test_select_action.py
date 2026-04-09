"""Testes para a ação de seleção (SelectAction)."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

import pytest
from unittest.mock import Mock, patch
from rpa.actions.base_action import BaseAction


def test_select_action_is_base_action_subclass():
    """Testa se SelectAction herda de BaseAction."""
    from rpa.actions.select_action import SelectAction

    assert issubclass(SelectAction, BaseAction)


def test_select_action_initialization():
    """Testa inicialização da SelectAction."""
    from rpa.actions.select_action import SelectAction

    # Testa inicialização sem config
    action1 = SelectAction()
    assert action1.config == {}
    assert action1.logger is None

    # Testa inicialização com config
    config = {'required': True, 'timeout': 5}
    action2 = SelectAction(config)
    assert action2.config == config
    assert action2.logger is None

    # Testa inicialização com logger
    mock_logger = Mock()
    action3 = SelectAction(config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


@patch('rpa.actions.select_action.type_text')
@patch('rpa.actions.select_action.click')
@patch('rpa.actions.select_action.find')
def test_select_action_execute_success(mock_find, mock_click, mock_type_text):
    """Testa execução bem-sucedida da SelectAction."""
    from rpa.actions.select_action import SelectAction

    action = SelectAction()
    mock_find.return_value = True  # Simula que encontrou o elemento

    # Executa ação
    result = action.execute('dropdown_field', 'option_value')

    assert result is True
    mock_find.assert_called_once_with('dropdown_field')
    mock_click.assert_called_once()
    mock_type_text.assert_any_call('option_value')
    mock_type_text.assert_any_call('{ENTER}')


@patch('rpa.actions.select_action.type_text')
@patch('rpa.actions.select_action.click')
@patch('rpa.actions.select_action.find')
def test_select_action_execute_without_value(mock_find, mock_click, mock_type_text):
    """Testa execução sem valor especificado."""
    from rpa.actions.select_action import SelectAction

    action = SelectAction()
    mock_find.return_value = True

    # Executa ação sem valor - deve levantar exceção
    with pytest.raises(ValueError, match="Valor não fornecido para seleção no campo"):
        action.execute('dropdown_field')

    # Não deve chamar as funções do BotCity
    mock_find.assert_not_called()
    mock_click.assert_not_called()
    mock_type_text.assert_not_called()


@patch('rpa.actions.select_action.type_text')
@patch('rpa.actions.select_action.click')
@patch('rpa.actions.select_action.find')
def test_select_action_execute_with_logger(mock_find, mock_click, mock_type_text):
    """Testa execução com logger."""
    from rpa.actions.select_action import SelectAction

    mock_logger = Mock()
    action = SelectAction({'required': True}, mock_logger)
    mock_find.return_value = True

    result = action.execute('dropdown_field', 'option_value')

    # Verifica que logger foi usado
    assert mock_logger.info.called
    assert result is True
    mock_find.assert_called_once_with('dropdown_field')
    mock_click.assert_called_once()
    mock_type_text.assert_any_call('option_value')
    mock_type_text.assert_any_call('{ENTER}')


def test_select_action_get_description():
    """Testa método get_description da SelectAction."""
    from rpa.actions.select_action import SelectAction

    action = SelectAction()
    assert action.get_description() == "select action"


@patch('rpa.actions.select_action.type_text')
@patch('rpa.actions.select_action.click')
@patch('rpa.actions.select_action.find')
def test_select_action_execute_with_custom_config(mock_find, mock_click, mock_type_text):
    """Testa execução com configuração personalizada."""
    from rpa.actions.select_action import SelectAction

    config = {'some_setting': 'value'}
    action = SelectAction(config)
    mock_find.return_value = True

    result = action.execute('field', 'value')
    assert result is True
    mock_find.assert_called_once_with('field')
    mock_click.assert_called_once()
    mock_type_text.assert_any_call('value')
    mock_type_text.assert_any_call('{ENTER}')


if __name__ == '__main__':
    # Executa todos os testes
    test_select_action_is_base_action_subclass()
    test_select_action_initialization()
    test_select_action_execute_success()
    test_select_action_execute_without_value()
    test_select_action_execute_with_logger()
    test_select_action_get_description()
    test_select_action_execute_with_custom_config()
    print("✓ Todos os testes de SelectAction passaram!")
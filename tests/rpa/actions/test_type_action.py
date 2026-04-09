"""Testes para a ação de digitação (TypeAction)."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

# Carregar mock do botcity antes de qualquer importação
import tests.mock_botcity

import pytest
from unittest.mock import Mock, patch
from rpa.actions.base_action import BaseAction


def test_type_action_is_base_action_subclass():
    """Testa se TypeAction herda de BaseAction."""
    from rpa.actions.type_action import TypeAction

    assert issubclass(TypeAction, BaseAction)


def test_type_action_initialization():
    """Testa inicialização da TypeAction."""
    from rpa.actions.type_action import TypeAction

    # Testa inicialização sem config
    action1 = TypeAction()
    assert action1.config == {}
    assert action1.logger is None

    # Testa inicialização com config
    config = {'required': True, 'timeout': 5}
    action2 = TypeAction(config)
    assert action2.config == config
    assert action2.logger is None

    # Testa inicialização com logger
    mock_logger = Mock()
    action3 = TypeAction(config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


def test_type_action_execute_success():
    """Testa execução bem-sucedida da TypeAction."""
    from rpa.actions.type_action import TypeAction

    action = TypeAction()

    # Mock das dependências externas
    with patch('rpa.actions.type_action.click_image') as mock_click, \
         patch('rpa.actions.type_action.type_text') as mock_type:

        # Configura mocks
        mock_click.return_value = None
        mock_type.return_value = None

        # Executa ação
        result = action.execute('username_field', 'john_doe')

        # Verifica chamadas
        mock_click.assert_called_once_with('username_field', 0.3)
        mock_type.assert_called_once_with('john_doe')
        assert result is True


def test_type_action_execute_with_custom_time_wait():
    """Testa execução com tempo de espera personalizado."""
    from rpa.actions.type_action import TypeAction

    config = {'time_wait': 1.0}
    action = TypeAction(config)

    with patch('rpa.actions.type_action.click_image') as mock_click, \
         patch('rpa.actions.type_action.type_text') as mock_type:

        mock_click.return_value = None
        mock_type.return_value = None

        result = action.execute('password_field', 'secret123')

        mock_click.assert_called_once_with('password_field', 1.0)
        mock_type.assert_called_once_with('secret123')
        assert result is True


def test_type_action_execute_with_logger():
    """Testa execução com logger."""
    from rpa.actions.type_action import TypeAction

    mock_logger = Mock()
    action = TypeAction({'required': True}, mock_logger)

    with patch('rpa.actions.type_action.click_image') as mock_click, \
         patch('rpa.actions.type_action.type_text') as mock_type:

        mock_click.return_value = None
        mock_type.return_value = None

        result = action.execute('email_field', 'test@example.com')

        # Verifica que logger foi usado
        assert mock_logger.info.called
        assert result is True


def test_type_action_execute_image_not_found():
    """Testa execução quando imagem não é encontrada."""
    from rpa.actions.type_action import TypeAction

    action = TypeAction()

    with patch('rpa.actions.type_action.click_image') as mock_click:
        mock_click.side_effect = Exception('Imagem não encontrada: username_field')

        # Deve levantar exceção
        with pytest.raises(Exception, match='Imagem não encontrada: username_field'):
            action.execute('username_field', 'john_doe')


def test_type_action_execute_type_error():
    """Testa execução quando ocorre erro na digitação."""
    from rpa.actions.type_action import TypeAction

    action = TypeAction()

    with patch('rpa.actions.type_action.click_image') as mock_click, \
         patch('rpa.actions.type_action.type_text') as mock_type:

        mock_click.return_value = None
        mock_type.side_effect = Exception('Erro na digitação')

        # Deve levantar exceção
        with pytest.raises(Exception, match='Erro na digitação'):
            action.execute('field', 'value')


def test_type_action_get_description():
    """Testa método get_description da TypeAction."""
    from rpa.actions.type_action import TypeAction

    action = TypeAction()
    assert action.get_description() == "type action"


if __name__ == '__main__':
    # Executa todos os testes
    test_type_action_is_base_action_subclass()
    test_type_action_initialization()
    test_type_action_execute_success()
    test_type_action_execute_with_custom_time_wait()
    test_type_action_execute_with_logger()
    test_type_action_execute_image_not_found()
    test_type_action_execute_type_error()
    test_type_action_get_description()
    print("✓ Todos os testes de TypeAction passaram!")
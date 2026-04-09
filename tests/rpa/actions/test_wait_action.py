"""Testes para a ação de espera (WaitAction)."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

# Carregar mock do botcity antes de qualquer importação
import tests.mock_botcity

import pytest
from unittest.mock import Mock, patch
from rpa.actions.base_action import BaseAction
import time


def test_wait_action_is_base_action_subclass():
    """Testa se WaitAction herda de BaseAction."""
    from rpa.actions.wait_action import WaitAction

    assert issubclass(WaitAction, BaseAction)


def test_wait_action_initialization():
    """Testa inicialização da WaitAction."""
    from rpa.actions.wait_action import WaitAction

    # Testa inicialização sem config
    action1 = WaitAction()
    assert action1.config == {}
    assert action1.logger is None

    # Testa inicialização com config
    config = {'required': True, 'timeout': 5}
    action2 = WaitAction(config)
    assert action2.config == config
    assert action2.logger is None

    # Testa inicialização com logger
    mock_logger = Mock()
    action3 = WaitAction(config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


def test_wait_action_execute_success():
    """Testa execução bem-sucedida da WaitAction."""
    from rpa.actions.wait_action import WaitAction

    action = WaitAction()

    # Mock time.sleep para não realmente esperar
    with patch('time.sleep') as mock_sleep:
        mock_sleep.return_value = None

        # Executa ação com tempo especificado
        result = action.execute('wait', '2.5')

        # Verifica chamadas
        mock_sleep.assert_called_once_with(2.5)
        assert result is True


def test_wait_action_execute_default_time():
    """Testa execução com tempo padrão (quando value é None)."""
    from rpa.actions.wait_action import WaitAction

    action = WaitAction()

    with patch('time.sleep') as mock_sleep:
        mock_sleep.return_value = None

        # Executa ação sem valor (deve usar 1.0 como padrão)
        result = action.execute('wait')

        mock_sleep.assert_called_once_with(1.0)
        assert result is True


def test_wait_action_execute_with_logger():
    """Testa execução com logger."""
    from rpa.actions.wait_action import WaitAction

    mock_logger = Mock()
    action = WaitAction({'required': True}, mock_logger)

    with patch('time.sleep') as mock_sleep:
        mock_sleep.return_value = None

        result = action.execute('wait', '3.0')

        # Verifica que logger foi usado
        assert mock_logger.info.called
        mock_sleep.assert_called_once_with(3.0)
        assert result is True


def test_wait_action_execute_invalid_time():
    """Testa execução com tempo inválido."""
    from rpa.actions.wait_action import WaitAction

    action = WaitAction()

    with patch('time.sleep') as mock_sleep:
        # Deve levantar exceção para valor não numérico
        with pytest.raises(Exception, match="Tempo de espera inválido: 'invalid'. Deve ser um número."):
            action.execute('wait', 'invalid')

        # Não deve chamar sleep
        mock_sleep.assert_not_called()


def test_wait_action_execute_negative_time():
    """Testa execução com tempo negativo (ainda válido para time.sleep)."""
    from rpa.actions.wait_action import WaitAction

    action = WaitAction()

    with patch('time.sleep') as mock_sleep:
        mock_sleep.return_value = None

        # time.sleep aceita 0 e valores negativos (trata como 0)
        result = action.execute('wait', '0')
        mock_sleep.assert_called_once_with(0.0)
        assert result is True


def test_wait_action_get_description():
    """Testa método get_description da WaitAction."""
    from rpa.actions.wait_action import WaitAction

    action = WaitAction()
    assert action.get_description() == "wait action"


def test_wait_action_execute_with_custom_config():
    """Testa execução com configuração personalizada."""
    from rpa.actions.wait_action import WaitAction

    # Config não afeta wait_action diretamente, mas testa que não quebra
    config = {'some_setting': 'value'}
    action = WaitAction(config)

    with patch('time.sleep') as mock_sleep:
        mock_sleep.return_value = None

        result = action.execute('wait', '1.5')
        mock_sleep.assert_called_once_with(1.5)
        assert result is True


if __name__ == '__main__':
    # Executa todos os testes
    test_wait_action_is_base_action_subclass()
    test_wait_action_initialization()
    test_wait_action_execute_success()
    test_wait_action_execute_default_time()
    test_wait_action_execute_with_logger()
    test_wait_action_execute_invalid_time()
    test_wait_action_execute_negative_time()
    test_wait_action_get_description()
    test_wait_action_execute_with_custom_config()
    print("✓ Todos os testes de WaitAction passaram!")
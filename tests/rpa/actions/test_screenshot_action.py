"""Testes para a ação de captura de tela (ScreenshotAction)."""
import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

import pytest
from unittest.mock import Mock, patch
from rpa.actions.base_action import BaseAction


def test_screenshot_action_is_base_action_subclass():
    """Testa se ScreenshotAction herda de BaseAction."""
    from rpa.actions.screenshot_action import ScreenshotAction

    assert issubclass(ScreenshotAction, BaseAction)


def test_screenshot_action_initialization():
    """Testa inicialização da ScreenshotAction."""
    from rpa.actions.screenshot_action import ScreenshotAction

    # Testa inicialização sem config
    action1 = ScreenshotAction()
    assert action1.config == {}
    assert action1.logger is None

    # Testa inicialização com config
    config = {'required': True, 'timeout': 5}
    action2 = ScreenshotAction(config)
    assert action2.config == config
    assert action2.logger is None

    # Testa inicialização com logger
    mock_logger = Mock()
    action3 = ScreenshotAction(config, mock_logger)
    assert action3.config == config
    assert action3.logger == mock_logger


@patch('os.makedirs')
@patch('datetime.datetime')
@patch('rpa.actions.screenshot_action.take_screenshot')
def test_screenshot_action_execute_success_without_path(mock_take_screenshot, mock_datetime, mock_makedirs):
    """Testa execução bem-sucedida da ScreenshotAction sem caminho especificado."""
    from rpa.actions.screenshot_action import ScreenshotAction

    # Configura mock do datetime
    mock_now = Mock()
    mock_now.strftime.return_value = "20250408_143025"
    mock_datetime.now.return_value = mock_now

    action = ScreenshotAction()

    # Executa ação sem caminho (deve gerar caminho automático)
    result = action.execute('login_screen')

    assert result is True
    mock_makedirs.assert_called_once_with('screenshots', exist_ok=True)
    mock_take_screenshot.assert_called_once_with('screenshots/login_screen_20250408_143025.png')


@patch('rpa.actions.screenshot_action.take_screenshot')
def test_screenshot_action_execute_success_with_path(mock_take_screenshot):
    """Testa execução bem-sucedida da ScreenshotAction com caminho especificado."""
    from rpa.actions.screenshot_action import ScreenshotAction

    action = ScreenshotAction()

    # Executa ação com caminho personalizado
    result = action.execute('error_screen', '/tmp/error.png')

    assert result is True
    mock_take_screenshot.assert_called_once_with('/tmp/error.png')


@patch('rpa.actions.screenshot_action.take_screenshot')
def test_screenshot_action_execute_with_logger(mock_take_screenshot):
    """Testa execução com logger."""
    from rpa.actions.screenshot_action import ScreenshotAction

    mock_logger = Mock()
    action = ScreenshotAction({'required': True}, mock_logger)

    result = action.execute('test_screen', '/tmp/test.png')

    # Verifica que logger foi usado
    assert mock_logger.info.called
    assert result is True
    mock_take_screenshot.assert_called_once_with('/tmp/test.png')


def test_screenshot_action_get_description():
    """Testa método get_description da ScreenshotAction."""
    from rpa.actions.screenshot_action import ScreenshotAction

    action = ScreenshotAction()
    assert action.get_description() == "screenshot action"


@patch('rpa.actions.screenshot_action.take_screenshot')
def test_screenshot_action_execute_with_custom_config(mock_take_screenshot):
    """Testa execução com configuração personalizada."""
    from rpa.actions.screenshot_action import ScreenshotAction

    config = {'some_setting': 'value'}
    action = ScreenshotAction(config)

    result = action.execute('config_screen', '/tmp/config.png')

    assert result is True
    mock_take_screenshot.assert_called_once_with('/tmp/config.png')


@patch('os.makedirs')
@patch('datetime.datetime')
@patch('rpa.actions.screenshot_action.take_screenshot')
def test_screenshot_action_execute_directory_creation(mock_take_screenshot, mock_datetime, mock_makedirs):
    """Testa criação de diretório screenshots quando não existe."""
    from rpa.actions.screenshot_action import ScreenshotAction

    action = ScreenshotAction()

    mock_now = Mock()
    mock_now.strftime.return_value = "20250408_143025"
    mock_datetime.now.return_value = mock_now

    result = action.execute('test')

    assert result is True
    mock_makedirs.assert_called_once_with('screenshots', exist_ok=True)
    mock_take_screenshot.assert_called_once_with('screenshots/test_20250408_143025.png')


@patch('rpa.actions.screenshot_action.take_screenshot')
def test_screenshot_action_execute_exception_handling(mock_take_screenshot):
    """Testa tratamento de exceções na ScreenshotAction."""
    from rpa.actions.screenshot_action import ScreenshotAction

    action = ScreenshotAction()

    # Simula falha na execução
    mock_take_screenshot.side_effect = Exception("Simulated error")

    with pytest.raises(Exception, match="Simulated error"):
        action.execute('failing_screen')


if __name__ == '__main__':
    # Executa todos os testes
    test_screenshot_action_is_base_action_subclass()
    test_screenshot_action_initialization()
    test_screenshot_action_execute_success_without_path()
    test_screenshot_action_execute_success_with_path()
    test_screenshot_action_execute_with_logger()
    test_screenshot_action_get_description()
    test_screenshot_action_execute_with_custom_config()
    test_screenshot_action_execute_directory_creation()
    test_screenshot_action_execute_exception_handling()
    print("✓ Todos os testes de ScreenshotAction passaram!")
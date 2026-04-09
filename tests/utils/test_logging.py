"""Testes para o sistema de logging do CeFal."""

import sys
import os
sys.path.insert(0, '/home/nmqvl/code/cefal')

import pytest
import logging
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from utils.logging import CeFalLogger, get_logger


class TestCeFalLogger:
    """Testes para a classe CeFalLogger."""

    def setup_method(self):
        """Configuração antes de cada teste."""
        self.temp_dir = tempfile.mkdtemp()
        self.workflow_name = "test_workflow"
        self.logger = CeFalLogger(self.workflow_name, self.temp_dir)

    def teardown_method(self):
        """Limpeza após cada teste."""
        # Remove diretório temporário
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_logger_initialization(self):
        """Testa inicialização do logger."""
        # Verifica se o diretório foi criado
        assert os.path.exists(self.temp_dir)

        # Verifica se o logger foi configurado
        assert self.logger.workflow_name == self.workflow_name
        assert self.logger.log_dir == self.temp_dir
        assert self.logger.logger.name == f"cefal.{self.workflow_name}"
        assert self.logger.logger.level == logging.DEBUG

        # Verifica se tem handlers
        assert len(self.logger.logger.handlers) == 2  # FileHandler + StreamHandler

    def test_info_log(self):
        """Testa log de nível INFO."""
        with patch.object(self.logger.logger, 'info') as mock_info:
            self.logger.info("Test message")
            mock_info.assert_called_once()
            assert "Test message" in mock_info.call_args[0][0]

    def test_info_log_with_metadata(self):
        """Testa log de nível INFO com metadados."""
        with patch.object(self.logger.logger, 'info') as mock_info:
            self.logger.info("Test message", action="click", field="button")
            mock_info.assert_called_once()
            log_message = mock_info.call_args[0][0]
            assert "Test message" in log_message
            assert "Action: click" in log_message
            assert "Field: button" in log_message

    def test_error_log(self):
        """Testa log de nível ERROR."""
        with patch.object(self.logger.logger, 'error') as mock_error:
            self.logger.error("Error message")
            mock_error.assert_called_once()
            assert "Error message" in mock_error.call_args[0][0]

    def test_error_log_with_exception(self):
        """Testa log de nível ERROR com exceção."""
        with patch.object(self.logger.logger, 'error') as mock_error:
            exception = ValueError("Invalid value")
            self.logger.error("Error message", error=exception)
            mock_error.assert_called_once()
            log_message = mock_error.call_args[0][0]
            assert "Error message" in log_message
            assert "ValueError" in log_message
            assert "Invalid value" in log_message

    def test_debug_log(self):
        """Testa log de nível DEBUG."""
        with patch.object(self.logger.logger, 'debug') as mock_debug:
            self.logger.debug("Debug message")
            mock_debug.assert_called_once()
            assert "Debug message" in mock_debug.call_args[0][0]

    def test_warning_log(self):
        """Testa log de nível WARNING."""
        with patch.object(self.logger.logger, 'warning') as mock_warning:
            self.logger.warning("Warning message")
            mock_warning.assert_called_once()
            assert "Warning message" in mock_warning.call_args[0][0]

    def test_start_workflow(self):
        """Testa log de início de workflow."""
        with patch.object(self.logger, 'info') as mock_info:
            self.logger.start_workflow()
            mock_info.assert_called_once()
            assert f"Starting workflow '{self.workflow_name}'" in mock_info.call_args[0][0]

    def test_start_workflow_with_config(self):
        """Testa log de início de workflow com configuração."""
        with patch.object(self.logger, 'info') as mock_info:
            config = {'timeout': 30, 'retry': 3}
            self.logger.start_workflow(config)
            mock_info.assert_called_once()
            log_message = mock_info.call_args[0][0]
            assert f"Starting workflow '{self.workflow_name}'" in log_message
            assert "'timeout': 30" in log_message
            assert "'retry': 3" in log_message

    def test_end_workflow_success(self):
        """Testa log de término de workflow com sucesso."""
        with patch.object(self.logger, 'info') as mock_info:
            self.logger.end_workflow(success=True, duration=5.25)
            mock_info.assert_called_once()
            log_message = mock_info.call_args[0][0]
            assert f"Workflow '{self.workflow_name}' completed with status: SUCCESS" in log_message
            assert "Duration: 5.25s" in log_message

    def test_end_workflow_failure(self):
        """Testa log de término de workflow com falha."""
        with patch.object(self.logger, 'info') as mock_info:
            self.logger.end_workflow(success=False)
            mock_info.assert_called_once()
            assert f"Workflow '{self.workflow_name}' completed with status: FAILED" in mock_info.call_args[0][0]

    def test_structure_message_without_metadata(self):
        """Testa estruturação de mensagem sem metadados."""
        result = self.logger._structure_message("Test message")
        assert result == "Test message"

    def test_structure_message_with_action(self):
        """Testa estruturação de mensagem com ação."""
        result = self.logger._structure_message("Test message", action="click")
        assert result == "Test message | Action: click"

    def test_structure_message_with_field(self):
        """Testa estruturação de mensagem com campo."""
        result = self.logger._structure_message("Test message", field="button")
        assert result == "Test message | Field: button"

    def test_structure_message_with_both(self):
        """Testa estruturação de mensagem com ação e campo."""
        result = self.logger._structure_message("Test message", action="click", field="button")
        assert result == "Test message | Action: click | Field: button"


class TestGetLogger:
    """Testes para a função get_logger."""

    def test_get_logger_creates_instance(self):
        """Testa se get_logger cria uma instância de CeFalLogger."""
        with tempfile.TemporaryDirectory() as temp_dir:
            logger = get_logger("test_workflow", temp_dir)
            assert isinstance(logger, CeFalLogger)
            assert logger.workflow_name == "test_workflow"
            assert logger.log_dir == temp_dir

    def test_get_logger_default_dir(self):
        """Testa se get_logger usa diretório padrão."""
        # Cria diretório logs se não existir
        if not os.path.exists("logs"):
            os.makedirs("logs")

        logger = get_logger("test_workflow")
        assert isinstance(logger, CeFalLogger)
        assert logger.workflow_name == "test_workflow"
        assert logger.log_dir == "logs"


def test_log_file_creation():
    """Testa se arquivo de log é criado."""
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = CeFalLogger("test_workflow", temp_dir)

        # Log uma mensagem
        logger.info("Test log message")

        # Verifica se arquivo foi criado
        log_files = [f for f in os.listdir(temp_dir) if f.endswith('.log')]
        assert len(log_files) == 1

        # Verifica conteúdo do arquivo
        log_file_path = os.path.join(temp_dir, log_files[0])
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test log message" in content


if __name__ == '__main__':
    # Executa todos os testes
    test_logger = TestCeFalLogger()
    test_logger.setup_method()

    test_logger.test_logger_initialization()
    test_logger.test_info_log()
    test_logger.test_info_log_with_metadata()
    test_logger.test_error_log()
    test_logger.test_error_log_with_exception()
    test_logger.test_debug_log()
    test_logger.test_warning_log()
    test_logger.test_start_workflow()
    test_logger.test_start_workflow_with_config()
    test_logger.test_end_workflow_success()
    test_logger.test_end_workflow_failure()
    test_logger.test_structure_message_without_metadata()
    test_logger.test_structure_message_with_action()
    test_logger.test_structure_message_with_field()
    test_logger.test_structure_message_with_both()

    test_logger.teardown_method()

    # Testes da função get_logger
    test_get_logger = TestGetLogger()
    test_get_logger.test_get_logger_creates_instance()
    test_get_logger.test_get_logger_default_dir()

    # Teste de criação de arquivo
    test_log_file_creation()

    print("✓ Todos os testes de logging passaram!")
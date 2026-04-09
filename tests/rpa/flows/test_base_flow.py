"""Testes para a classe base BaseFlow."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import unittest
from unittest.mock import Mock, patch
from rpa.flows.base_flow import BaseFlow


class TestBaseFlow(unittest.TestCase):
    """Testes para a classe BaseFlow."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.workflow_config = {
            'template': 'test_template',
            'description': 'Test workflow',
            'flow_type': 'test',
            'steps': ['step1', 'step2'],
            'actions': [
                {'type': 'type', 'field': 'field1', 'required': True},
                {'type': 'click', 'field': 'button1', 'action': 'final'}
            ]
        }
        self.data = [{'field1': 'value1'}, {'field1': 'value2'}]

    def test_base_flow_is_abstract(self):
        """Testa se BaseFlow é uma classe abstrata."""
        with self.assertRaises(TypeError):
            BaseFlow(self.workflow_config, self.data)

    def test_concrete_flow_implementation(self):
        """Testa se uma classe concreta pode ser instanciada."""
        class ConcreteFlow(BaseFlow):
            def execute(self):
                return "executed"

        flow = ConcreteFlow(self.workflow_config, self.data)
        self.assertIsInstance(flow, BaseFlow)
        self.assertEqual(flow.config, self.workflow_config)
        self.assertEqual(flow.data, self.data)
        self.assertEqual(flow.template, 'test_template')

    def test_get_steps_method(self):
        """Testa o método get_steps."""
        class ConcreteFlow(BaseFlow):
            def execute(self):
                pass

        flow = ConcreteFlow(self.workflow_config, self.data)
        steps = flow.get_steps()
        self.assertEqual(steps, ['step1', 'step2'])

    def test_get_actions_method(self):
        """Testa o método get_actions."""
        class ConcreteFlow(BaseFlow):
            def execute(self):
                pass

        flow = ConcreteFlow(self.workflow_config, self.data)
        actions = flow.get_actions()
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0]['type'], 'type')
        self.assertEqual(actions[1]['type'], 'click')

    @patch('rpa.flows.take_initial_steps.take_initial_steps')
    def test_execute_initial_steps_method(self, mock_take_initial_steps):
        """Testa o método execute_initial_steps."""
        class ConcreteFlow(BaseFlow):
            def execute(self):
                pass

        flow = ConcreteFlow(self.workflow_config, self.data)
        flow.execute_initial_steps()

        mock_take_initial_steps.assert_called_once_with('test_template', ['step1', 'step2'])

    def test_flow_with_default_template(self):
        """Testa flow sem template específico."""
        config_without_template = {
            'description': 'Test workflow',
            'flow_type': 'test',
            'steps': ['step1'],
            'actions': [{'type': 'type', 'field': 'field1'}]
        }

        class ConcreteFlow(BaseFlow):
            def execute(self):
                pass

        flow = ConcreteFlow(config_without_template, self.data)
        self.assertEqual(flow.template, 'default')

    def test_flow_with_empty_steps(self):
        """Testa flow sem steps definidos."""
        config_without_steps = {
            'template': 'test',
            'description': 'Test workflow',
            'flow_type': 'test',
            'actions': [{'type': 'type', 'field': 'field1'}]
        }

        class ConcreteFlow(BaseFlow):
            def execute(self):
                pass

        flow = ConcreteFlow(config_without_steps, self.data)
        steps = flow.get_steps()
        self.assertEqual(steps, [])

    def test_flow_with_empty_actions(self):
        """Testa flow sem actions definidas."""
        config_without_actions = {
            'template': 'test',
            'description': 'Test workflow',
            'flow_type': 'test',
            'steps': ['step1']
        }

        class ConcreteFlow(BaseFlow):
            def execute(self):
                pass

        flow = ConcreteFlow(config_without_actions, self.data)
        actions = flow.get_actions()
        self.assertEqual(actions, [])


if __name__ == '__main__':
    unittest.main()
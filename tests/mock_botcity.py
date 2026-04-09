"""Mock do módulo botcity para permitir testes sem dependência instalada."""

import sys
from unittest.mock import Mock

# Mock do botcity.core.DesktopBot
class MockDesktopBot:
    def __init__(self):
        self.state = Mock(map_images={})

    def find(self, label, matching=0.95):
        return True

    def click(self):
        pass

    def type_keys(self, text):
        pass

    def scroll_down(self, amount):
        pass

    def add_image(self, label, path):
        if not hasattr(self.state, 'map_images'):
            self.state.map_images = {}
        self.state.map_images[label] = path

# Mock completo do módulo botcity
mock_botcity = Mock()
mock_botcity.core = Mock()
mock_botcity.core.DesktopBot = MockDesktopBot

# Injetar mock no sys.modules
sys.modules['botcity'] = mock_botcity
sys.modules['botcity.core'] = mock_botcity.core
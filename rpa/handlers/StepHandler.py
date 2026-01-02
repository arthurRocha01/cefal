from ..lib.BotCityLib import BotCityLib
from pathlib import Path
import re

class StepHandler:
    def __init__(self, template):
        self.template = template
        self.bot = BotCityLib(template)
        self.path = Path(f'resources/templates/{template}/steps')

    def _get_steps_path(self):
        return list(self.path.glob('*.png'))
    
    def take_steps(self):
        """Executa os passos necessários para o registro."""
        for step in self._get_steps_path():
            step_name = step.stem
            print(f'Executando passo: {step_name}')
            self.bot.click_in_field(step_name)
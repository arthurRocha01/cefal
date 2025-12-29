from ..lib.BotCityLib import BotCityLib
from pathlib import Path
import re

class StepHandler:
    def __init__(self, template):
        self.template = template
        self.bot = BotCityLib(template)
        self.path = Path(f'resources/templates/{template}/steps')

    def _sort_steps(self, steps):
        return sorted(steps, key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x.stem)])
    
    def _get_steps_path(self):
        steps = list(self.path.glob('*.png'))
        return self._sort_steps(steps)

    def take_steps(self):
        """Executa os passos necessários para o registro."""
        for step in self._get_steps_path():
            step_name = step.stem
            print(f'Executando passo: {step_name}')
            self.bot.click_in_field(step_name)
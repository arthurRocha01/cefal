from ..lib.BotCityLib import BotCityLib
import re
from pathlib import Path

class ExecutionHandler:
  def __init__(self, template):
    self.bot = BotCityLib(template)
    self.path = Path(f'resources/templates/{template}')

  def _sort_steps(self, steps):
    return sorted(steps, key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x.stem)])
    
  def _get_steps_path(self):
    steps = list(self.path / 'steps'.glob('*.png'))
    return self._sort_steps(steps)
  
  def _start_steps(self):
    for step in self._get_steps_path():
      step_name = step.stem
      print(f'Executando passo: {step_name}')
      self.bot.write(step_name, 'text')

  def _entter_data(self, item_dict):
    for i, value in enumerate(item_dict):
      label = self.bot.images_mapped[i]
      print(f'Preenchendo {label} com {value}')
      self.bot.write(label, value)

  def _save_action(self):
    self.bot.scroll_screen(15)
    self.bot.click_in_field('save')

  def save(self, data):
    """ Determina as operações para salvar o registro. """
    for item in data:
      self._entter_data(item)
      self._save_action()

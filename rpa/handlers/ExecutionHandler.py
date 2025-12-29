from lib.BotCityLib import BotCityLib
import re

class ExecutionHandler:
  def __init__(self):
    self.bot = BotCityLib('register')

  def _sort_steps(self, steps):
    return sorted(steps, key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x.stem)])
    
  def _get_steps_path(self):
    steps = list(self.path.glob('*.png'))
    return self._sort_steps(steps)

  def save(self):
    """ Determina as operações para salvar o registro. """
    for step in self._get_steps_path():
      step_name = step.stem
      print(f'Executando passo: {step_name}')
      self.bot.write(step_name, 'text')

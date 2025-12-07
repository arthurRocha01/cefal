from botcity.core import DesktopBot
from utils import slows_flow

class HandlerRegister:
  def __init__(self, matching=0.95):
    self.desktop = DesktopBot()
    self.matching = matching
  
  def _click_in_field(self, template, clicks=1):
    """Clica na imagem especificada pelo template."""
    if not self.desktop.find(template, matching=self.matching):
      raise Exception(f'Imagem não encontrada: {template}')
    
    self.desktop.click()
    slows_flow()

  def write(self, template, text):
    """Escreve o texto no campo identificado pela imagem template."""
    self._click_in_field(template)
    self.desktop.type_keys(text)

  def save(self):
    """Salva o produto clicando no botão de salvar."""
    self._click_in_field('save_button.png')

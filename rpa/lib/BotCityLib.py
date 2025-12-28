from botcity.core import DesktopBot
from utils import slows_flow

class BotCityLib:
    def __init__(self, template, matching=0.95):
        self.template = template
        self.desktop = DesktopBot()
        self.matching = matching

    def _get_corresponding_image(self, field):
        """Retorna o caminho da imagem correspondente ao campo."""
        return f'resources/{self.template}/executions/{field}.png'

    def _click_in_field(self, template, clicks=1):
        """Clica na imagem especificada pelo template."""
        if not self.desktop.find(template, matching=self.matching):
            raise Exception(f'Imagem não encontrada: {template}')
        
        self.desktop.click()
        slows_flow()

    def write(self, field, text):
        """Escreve o texto no campo identificado pela imagem template."""
        self._click_in_field(self._get_corresponding_image(field))
        self.desktop.type_keys(text)

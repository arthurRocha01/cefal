from botcity.core import DesktopBot
from .ImageFileLoader import ImageFileLoader
from ..utils import slows_flow
import os

class BotCityLib:
    def __init__(self, template, matching=0.95):
        self.template = template
        self.desktop = DesktopBot()
        self.matching = matching
        self.base_dir = os.getcwd()
        self.image_loader = ImageFileLoader(template)

        self._initialize_resources_template()

    def _initialize_resources_template(self):
        """Inicializa os recursos de template de imagens."""
        self.image_loader.upload_images_files(self)

        self.images_mapped = list(self.desktop.state.map_images.keys())
        print(f'Imagens mapeadas: {self.images_mapped}')

    def scroll_screen(self, clicks):
        self.desktop.scroll_down(clicks)

    def click_in_field(self, label, clicks=1):
        """Clica na imagem especificada pelo template."""
        print(label)
        if not self.desktop.find(label, matching=self.matching):
            raise Exception(f'Imagem não encontrada: {label}')
        
        self.desktop.click()
        slows_flow()

    def write(self, label, text):
        """Escreve o texto no campo identificado pela imagem template."""
        self.click_in_field(label)
        self.desktop.type_keys(text)

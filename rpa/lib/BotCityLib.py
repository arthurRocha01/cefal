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
        self.images = {}

        self._initialize_resources_template()

    def _initialize_resources_template(self):
        """Inicializa os recursos de template de imagens."""
        self.images = self.image_loader.upload_images_files(self)
        print(f'Imagens mapeadas: {list(self.desktop.state.map_images.keys())}')

    def click_in_field(self, template, clicks=1):
        """Clica na imagem especificada pelo template."""
        print(f'Buscando por: {template}')
        if not self.desktop.find(template, matching=self.matching):
            raise Exception(f'Imagem não encontrada: {template}')
        
        self.desktop.click()
        slows_flow()

    def write(self, field, text):
        """Escreve o texto no campo identificado pela imagem template."""
        self._click_in_field(self._get_corresponding_image(field), type)
        self.desktop.type_keys(text)

from rpa.handlers.HandlerRegister import HandlerRegister
import config.settings as settings

class Register:
    def __init__(self, handler: HandlerRegister):
        self.fields = settings.FIELDS
        self.handler = handler

    def run(self):
        """Executa o registro dos produtos com base nos dados passados."""
        pass
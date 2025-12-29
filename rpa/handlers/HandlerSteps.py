from ..lib.BotCityLib import BotCityLib

class HandlerSteps:
    def __init__(self, template):
        self.template = template
        self.bot = BotCityLib(template)

    def take_steps(self):
        """Executa os passos necessários para o registro."""
        for step in self.bot.images_mapped:
            print(f'Executando passo: {step}')
            self.bot.click_in_field(step)
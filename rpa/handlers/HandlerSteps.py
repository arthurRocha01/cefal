from ..lib.BotCityLib import BotCityLib

class HandlerSteps:
    def __init__(self, template):
        self.template = template
        self.bot = BotCityLib(template)

    def take_steps(self):
        """Executa os passos necessários para o registro."""
        self.bot.click_in_field('cadastro')
        print('Clicou no campo de cadastro.')
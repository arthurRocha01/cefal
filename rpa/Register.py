from rpa.handlers.ExecutionHandler import ExecutionHandler
from rpa.handlers.StepHandler import StepHandler

class Register:
    def __init__(self):
        self.template = 'register'
        self.execution_handler = ExecutionHandler(self.template)
        self.step_handler = StepHandler(self.template)

        self.fields = [
            'name', 'barcode', 'quantity', 'price', 'wholesale_price', 'wholesale_minimun_quantity'
        ]
        self.buttons = [
            'save'
        ]

    def run(self, data):
        """Executa o registro dos produtos com base nos dados passados."""
        try:
            self.step_handler.take_steps()
        except Exception:
            print('Erro ao executar passos iniciais.')
        
        self.execution_handler.save(data)
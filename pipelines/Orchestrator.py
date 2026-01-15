from interface.ProcessInterface import ProcessInterface
from rpa.flows import take_initial_steps
from rpa.flows import register_product

from pathlib import Path

class Orchestrator:
    def __init__(self):
        self.data_file_path = next(Path('resources/data').iterdir())
        self.proccess_interface = ProcessInterface()

    def start_process(self):
        """Inicia o processo de automação."""
        data = self.proccess_interface.read_csv(self.data_file_path)
        print(f'Dados lidos: {data[0]}')
        try:
            take_initial_steps.take_initial_steps()
        except Exception:
            print('Sem passos iniciais para executar.')
        register_product.register_products(data)
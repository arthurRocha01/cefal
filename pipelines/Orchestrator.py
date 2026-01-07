from interface.ProcessInterface import ProcessInterface
from rpa.flows import take_initial_steps
from rpa.flows import register_product

class Orchestrator:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.proccess_interface = ProcessInterface()

    def start_process(self):
        """Inicia o processo de automação."""
        data = self.proccess_interface.read_csv(self.data_file_path)
        print(f'Dados lidos: {data[0]}')
        # take_initial_steps.take_initial_steps()
        register_product.register_products(data)

from interface.ProcessInterface import ProcessInterface
from rpa.Register import Register

class Orchestrator:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.proccess_interface = ProcessInterface()
        self.register = Register()

    def start_process(self):
        """Inicia o processo de automação."""
        data = self.proccess_interface.read_csv(self.data_file_path)
        print(f'Dados lidos: {data[0]}')
        self.register.run(data)
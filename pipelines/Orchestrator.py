from ..interface.ProcessInterface import ProcessInterface
from rpa.handlers.StepHandler import StepHandler

class Orchestrator:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.proccess_interface = ProcessInterface()
        self.steps_handler = StepHandler('register')

    def start_process(self):
        """Inicia o processo de automação."""
        data = self.proccess_interface.read_csv(self.data_file_path)
        pass
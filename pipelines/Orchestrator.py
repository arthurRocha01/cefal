from interface.ProcessInterface import ProcessInterface
from rpa.HandlerRegister import HandlerRegister

class Orchestrator:
    def __init__(self):
        self.process_interface = ProcessInterface()
        self.register_handler = HandlerRegister()

    def start_process(self):
        pass
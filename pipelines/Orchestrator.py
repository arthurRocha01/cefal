# from interface.ProcessInterface import ProcessInterface
# from rpa.handlers.HandlerRegister import HandlerRegister
from rpa.handlers.HandlerSteps import HandlerSteps

class Orchestrator:
    def __init__(self):
        # self.process_interface = ProcessInterface()
        # self.register_handler = HandlerRegister()
        self.steps_handler = HandlerSteps('register')

    def start_process(self):
        self.steps_handler.take_steps()
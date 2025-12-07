from pipelines.Orchestrator import Orchestrator
from config.settings import *

def main():
    orchestrator = Orchestrator()
    orchestrator.start_process()

if __name__ == '__main__':
    main()

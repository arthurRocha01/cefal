from pipelines.Orchestrator import Orchestrator

def main():
    orchestrator = Orchestrator('resources/data/produtos.csv')
    orchestrator.start_process()

if __name__ == '__main__':
    main()

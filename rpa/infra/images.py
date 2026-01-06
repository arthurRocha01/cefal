from pathlib import Path

BASE = Path('resources/templates')

def img(template, name):
    return str(BASE / template / 'executions' / f'{name}.png')
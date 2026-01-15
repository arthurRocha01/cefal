# Configurações do RPA
TIME_WAIT = 0.7
MATCHING = 0.90


REGISTER = {
    'register': {
        'steps': ['register', 'products', 'add'],
        'executions': ['name', 'barcode', 'quantity', 'price', 'wholesale_price', 'wholesale_minimum_quantity', 'save'],
    }
}

# Configurações de Logging
LOG_DIR = 'logs'


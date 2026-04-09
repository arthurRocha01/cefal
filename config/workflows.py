"""Configuração de múltiplos workflows para o CeFal."""

WORKFLOWS = {
    'cadastro_produtos': {
        'template': 'register',
        'description': 'Cadastro de produtos no sistema ERP',
        'flow_type': 'registration',
        'steps': ['register', 'products', 'add'],
        'actions': [
            {'type': 'type', 'field': 'name', 'required': True},
            {'type': 'type', 'field': 'barcode', 'required': False},
            {'type': 'type', 'field': 'quantity', 'required': True},
            {'type': 'type', 'field': 'price', 'required': True},
            {'type': 'type', 'field': 'wholesale_price', 'required': False},
            {'type': 'type', 'field': 'wholesale_minimum_quantity', 'required': False},
            {'type': 'click', 'field': 'save', 'action': 'final'},
        ],
        'data_mapping': {
            'csv_columns': ['nome', 'codigo_barras', 'quantidade', 'preco', 'preco_atacado', 'quantidade_minima_atacado'],
            'field_mapping': {
                'nome': 'name',
                'codigo_barras': 'barcode',
                'quantidade': 'quantity',
                'preco': 'price',
                'preco_atacado': 'wholesale_price',
                'quantidade_minima_atacado': 'wholesale_minimum_quantity'
            }
        }
    }
}
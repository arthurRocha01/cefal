from rpa.infra.bootstrap import with_template
from rpa.actions.type import type_in
from rpa.actions.click import click_image
from rpa.infra.botcity import scroll
from config.rpa_settings import REGISTER
from rpa.flows.generic_flow import GenericFlow

TEMPLATE = 'register'

@with_template(TEMPLATE, 'executions')
def register_products(data):
    """Função de compatibilidade para cadastro de produtos.

    Usa internamente o GenericFlow da nova arquitetura.
    """
    print("⚠️  Usando função de compatibilidade register_products()")
    print("⚠️  Considere migrar para GenericFlow.from_workflow_name('cadastro_produtos', data)")

    # Converte dados para o formato esperado pelo novo workflow
    converted_data = []
    for item in data:
        # Mapeia campos antigos para novos
        converted_item = {
            'nome': item.get('name', ''),
            'codigo_barras': item.get('barcode', ''),
            'quantidade': item.get('quantity', ''),
            'preco': item.get('price', ''),
            'preco_atacado': item.get('wholesale_price', ''),
            'quantidade_minima_atacado': item.get('wholesale_minimum_quantity', '')
        }
        converted_data.append(converted_item)

    # Executa usando a nova arquitetura
    flow = GenericFlow.from_workflow_name('cadastro_produtos', converted_data)
    results = flow.execute()

    # Retorna resultados no formato antigo (para compatibilidade)
    return results
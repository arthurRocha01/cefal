from rpa.infra.bootstrap import with_template
from rpa.actions.type import type_in
from rpa.actions.click import click_image
from rpa.infra.botcity import scroll
from config.rpa_settings import REGISTER

TEMPLATE = 'register'

@with_template(TEMPLATE, 'executions')
def register_products(data):
    for item in data:
        for field in REGISTER[TEMPLATE]['executions'][:-1]: # Exclui o último campo (botão salvar)
            print(f'Typing in field: {field} with value: {item[field]}')
            type_in(field, item[field])
            if field == 'name':
                scroll(7)
        print('Clicked on save button')
        scroll(7)
        click_image('save')
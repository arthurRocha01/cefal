from rpa.infra.bootstrap import with_template
from rpa.actions.type import type_in
from rpa.actions.click import click_image
from rpa.infra.botcity import scroll
from config.rpa_settings import REGISTER
from rpa.infra.view import show_product, show_field, show_success, show_error

TEMPLATE = 'register'

@with_template(TEMPLATE, 'executions')
def register_products(data):
    for item in data:
        show_product(item)

        try:
            for field in REGISTER[TEMPLATE]['executions'][:-1]: # Exclui o último campo (botão salvar)

                show_field(field)
                type_in(field, item[field])

                if field == 'name':
                    scroll(7)

            scroll(7)
            click_image('save')

            show_success()
        except Exception as e:
            show_error(str(e))
            raise

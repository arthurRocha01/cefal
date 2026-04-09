from rpa.infra.bootstrap import with_template
from rpa.actions.click import click_image
from rpa.infra.images import get_label_from_image_path
from config.rpa_settings import REGISTER

def take_initial_steps(template='register', steps=None):
    """
    Executa os passos iniciais de um workflow.

    Args:
        template (str): Nome do template a ser usado
        steps (list): Lista de passos a serem executados
    """
    if steps is None:
        steps = REGISTER.get(template, {}).get('steps', [])

    @with_template(template, 'steps')
    def _execute_steps():
        for step in steps:
            print(f'Clicked on image: {get_label_from_image_path(step)}')
            click_image(get_label_from_image_path(step))

    return _execute_steps()
from rpa.infra.bootstrap import with_template
from rpa.actions.click import click_image
from rpa.infra.images import get_label_from_image_path
from config.rpa_settings import REGISTER

TEMPLATE = 'register'

@with_template(TEMPLATE, 'steps')
def take_initial_steps():
    for step in REGISTER['register']['steps']:
        print(f'Clicked on image: {get_label_from_image_path(step)}')
        click_image(get_label_from_image_path(step))
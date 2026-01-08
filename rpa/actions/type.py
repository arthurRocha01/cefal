from rpa.actions.click import click_image
from rpa.infra.botcity import type_text

def type_in(label, text, time_wait=0.3):
    click_image(label, time_wait)
    type_text(text)
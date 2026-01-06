from rpa.infra import botcity
from time import sleep

def click_image(label, time_wait=0.3):
    if not botcity.find(label):
        raise Exception(f'Imagem não encontrada: {label}')
    botcity.click()
    sleep(time_wait)
from botcity.core import DesktopBot
from config.rpa_settings import TIME_WAIT
from config.rpa_settings import MATCHING

_bot = DesktopBot()
_bot.wait(TIME_WAIT)

def find(label, matching=MATCHING):
    return _bot.find(label, matching=matching)

def click():
    _bot.click()

def type_text(text):
    _bot.type_keys(text)

def scroll(amount):
    _bot.scroll_down(amount)

def add_img(label, path):
    _bot.add_image(label, path)
    print(f'Mapped images: {list(_bot.state.map_images.keys())}')

def clear_images():
    _bot.state.map_images.clear()
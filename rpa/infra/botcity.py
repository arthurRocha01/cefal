from botcity.core import DesktopBot

_bot = DesktopBot()

def find(label, matching=0.95):
    return _bot.find(label, matching=matching)

def click():
    _bot.click()

def type_text(text):
    _bot.type_keys(text)

def scroll(direction, amount=100):
    """Realiza rolagem na direção especificada.

    Args:
        direction (str): Direção da rolagem ('up', 'down')
        amount (int): Quantidade de rolagem em pixels

    Note:
        Atualmente só suporta 'up' e 'down' pois o DesktopBot não tem
        métodos nativos para scroll left/right.
    """
    direction = direction.lower()
    if direction == 'up':
        _bot.scroll_up(amount)
    elif direction == 'down':
        _bot.scroll_down(amount)
    else:
        raise ValueError(f"Direção inválida: {direction}. Use: 'up', 'down'")

def add_img(label, path):
    _bot.add_image(label, path)
    print(f'Mapped images: {list(_bot.state.map_images.keys())}')

def clear_images():
    _bot.state.map_images.clear()

def take_screenshot(path):
    """Tira uma captura de tela e salva no caminho especificado."""
    _bot.screenshot(path)
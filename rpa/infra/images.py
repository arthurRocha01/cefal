from pathlib import Path
from config.rpa_settings import REGISTER

BASE = Path('resources/templates')

def get_image_paths(template, img_type):
    return [
        BASE / template / img_type / f'{img}.png'
        for img in REGISTER[template][img_type]
    ]

def get_label_from_image_path(image_path):
    return Path(image_path).stem
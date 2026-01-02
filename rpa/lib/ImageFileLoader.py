from pathlib import Path
import re

class ImageFileLoader:
    def __init__(self, template):
        self.path = Path('resources') / 'templates' / template
        self.extension = '.png'

    def _get_clear_label(self, raw_key):
        return re.sub(r'^\d{2}_', '', raw_key)

    def _upload_images_files_from_category(self, category):
        final_path = self.path / category

        if not final_path.exists():
            print(f'Aviso: Diretório {final_path} não encontrado.')
            return
        
        
        for image_file in final_path.glob(f'*{self.extension}'):
            yield {
                'label': image_file.stem,
                'path': str(image_file.resolve()),
            }

    def upload_images_files(self, bot):
        for category in ['steps', 'executions']:
            images = list(self._upload_images_files_from_category(category))
            images.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x['label'])])
            for image in images:
                bot.desktop.add_image(self._get_clear_label(image['label']), image['path'])
                print(f'Imagem carregada: {image["label"]} do diretório {category}')
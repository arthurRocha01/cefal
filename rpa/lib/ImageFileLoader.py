from pathlib import Path

class ImageFileLoader:
    def __init__(self, template):
        self.path = Path('resources') / 'templates' / template
        self.extension = '.png'

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
            for image in self._upload_images_files_from_category(category):
                bot.desktop.add_image(image['label'], image['path'])
                print(f'Imagem carregada: {image["label"]} do diretório {category}')
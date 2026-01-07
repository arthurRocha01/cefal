from rpa.infra.botcity import add_img
from rpa.infra.images import get_image_paths
from rpa.infra.images import get_label_from_image_path

def with_template(template, group):
    def decorator(flow):
        def wrapped(*args, **kwargs):
            for img_path in get_image_paths(template, group):
                add_img(
                    get_label_from_image_path(img_path),
                    img_path
                )
            return flow(*args, **kwargs)
        return wrapped
    return decorator
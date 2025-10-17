import os.path

from backend.core.path_conf import BASE_PATH
from backend.utils.import_parse import get_model_objects


def get_app_models() -> list[type]:
    """获取 app 所有模型类"""
    app_path = BASE_PATH / 'app'
    list_dirs = os.listdir(app_path)

    apps = [d for d in list_dirs if os.path.isdir(os.path.join(app_path, d)) and d != '__pycache__']

    objs = []
    for app in apps:
        module_path = f'backend.app.{app}.model'
        obj = get_model_objects(module_path)
        if obj:
            objs.extend(obj)

    return objs


# import all app models for auto create db tables
for cls in get_app_models():
    class_name = cls.__name__
    if class_name not in globals():
        globals()[class_name] = cls

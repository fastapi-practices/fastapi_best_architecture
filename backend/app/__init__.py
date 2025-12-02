from backend.utils.import_parse import get_all_models

# import all models for auto create db tables
for cls in get_all_models():
    class_name = cls.__name__
    if class_name not in globals():
        globals()[class_name] = cls

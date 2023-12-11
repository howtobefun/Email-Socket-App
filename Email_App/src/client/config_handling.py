from json import load
from types import SimpleNamespace

def init_config_data():
    config_file_path = 'src/config/config.json'
    with open(config_file_path) as fp:
        config_data_object = load(fp, object_hook=lambda d: SimpleNamespace(**d))

    return config_data_object
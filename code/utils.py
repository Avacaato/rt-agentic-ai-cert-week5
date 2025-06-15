import yaml
from paths import CONFIG_FILE_PATH


def load_config(config_path: str = CONFIG_FILE_PATH):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

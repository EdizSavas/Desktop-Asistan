import os
import json

def get_config_path(name):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    config_dir = os.path.join(base_dir, "config")

    if name == "gui_config":
        return os.path.join(config_dir, "gui_config.json")
    elif name == "shortcut_config":
        return os.path.join(config_dir, "shortcut_config.json")
    else:
        raise ValueError(f"Bilinmeyen config: {name}")

def load_config(name):
    path = get_config_path(name)
    with open(path, "r") as f:
        return json.load(f)

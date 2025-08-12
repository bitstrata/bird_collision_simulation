import json
import os

class ConfigLoader:
    def __init__(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def get(self, key, default=None):
        return self.config.get(key, default)

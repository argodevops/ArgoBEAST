from deepmerge import always_merger
from importlib import resources
from copy import deepcopy
import yaml
import os
import logging


class ConfigLoader():
    def __init__(self):
        # figure out where defaults.yaml is inside the package
        self.default_config = None
        self.user_config = None
        self.logger = logging.getLogger(__name__)

    def load(self, user_path: str = None) -> dict:
        self.default_config = self._load_internal_defaults()
        if user_path:
            if os.path.exists(user_path):
                self.user_config = self._load_yaml(user_path)
            else:
                self.logger.warning(
                    "No user config can be found, using defaults")
                self.user_config = {}
        else:
            self.user_config = {}

        return self._deep_merge(self.default_config, self.user_config)

    def _load_yaml(self, path) -> dict:
        try:
            yaml_file = yaml.safe_load(open(path))
            return yaml_file or {}
        except Exception as e:
            self.logger.error(f"Error loading yaml file: {e}")
            return {}

    def _load_internal_defaults(self) -> dict:
        source = resources.files(
            "test_framework.config").joinpath("defaults.yml")
        with resources.as_file(source) as f:
            data = self._load_yaml(f)
        return data or {}

    def _deep_merge(self, base: dict, override: dict) -> dict:
        new_base = deepcopy(base)
        config = always_merger.merge(new_base, override)
        return config

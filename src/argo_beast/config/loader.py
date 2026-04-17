import os
import logging
from importlib import resources
from copy import deepcopy
from deepmerge import always_merger
import yaml


class ConfigLoader:
    """
    ConfigLoader is responsible for loading and merging configuration files
    """

    def __init__(self):
        # figure out where defaults.yaml is inside the package
        self.default_config = None
        self.user_config = None
        self.logger = logging.getLogger(__name__)

    def load(self, user_path: str = None) -> dict:
        """
        Load and merge default and user configuration files
        :param user_path: Path to user configuration file
        :return: Merged configuration dictionary
        """
        self.default_config = self._load_internal_defaults()
        if user_path:
            if os.path.exists(user_path):
                self.user_config = self._load_yaml(user_path)
            else:
                self.logger.warning("No user config can be found, using defaults")
                self.user_config = {}
        else:
            self.user_config = {}

        return self._deep_merge(self.default_config, self.user_config)

    def _load_yaml(self, path) -> dict:
        """
        Load a YAML file from the given path
        :param path: Path to YAML file
        :return: Parsed YAML as dictionary
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                yaml_file = yaml.safe_load(f)
                return yaml_file or {}
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error(f"Error loading yaml file: {e}")
            return {}

    def _load_internal_defaults(self) -> dict:
        """
        Load the default configuration from the package resources
        :return: Default configuration dictionary
        """
        source = resources.files("argo_beast.config").joinpath("defaults.yml")
        with resources.as_file(source) as f:
            try:
                data = self._load_yaml(f)
            except Exception as e:
                self.logger.error(
                    f"Internal defaults missing, try reinstalling ArgoBEAST: {e}"
                )
        return data or {}

    def _deep_merge(self, base: dict, override: dict) -> dict:
        """
        Deep merge two dictionaries
        :param base: Base dictionary
        :param override: Override dictionary
        :return: Merged dictionary
        """
        new_base = deepcopy(base)
        config = always_merger.merge(new_base, override)
        return config

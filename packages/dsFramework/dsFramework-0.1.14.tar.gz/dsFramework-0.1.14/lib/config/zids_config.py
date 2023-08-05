"""
ZIDS config class
"""
import json


class ZIDSConfig:
    """
    class that store all configurations.
    """

    def __init__(self, custom_defaults: dict = {}):
        self.defaults = {}
        self.custom_config = custom_defaults

    def save(self, name: str, obj) -> None:
        """
        saving a object in configuration file
        :param name: the name of object
        :param obj: the object
        """
        self.custom_config[name] = obj

    def get(self, name: str):
        """
        return object from config (return default value if the configuration isn't supplied)
        :param name: the name of the object
        :return: the object
        """
        if name in self.custom_config:
            return self.custom_config[name]
        if name in self.defaults:
            return self.defaults[name]
        else:
            raise ValueError

    def dump_configuration(self, path: str) -> None:
        """
        dump configuration into file
        :param path: the path of the configuration file
        """
        with open(path, 'w') as f:
            json.dump({**self.defaults, **self.custom_config}, f)

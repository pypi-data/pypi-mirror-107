import ggwp
import os
import configparser

class EzConfig:
    def __init__(self):
        self.__path__ = ggwp.__file__

    def get_config(self, section, key):
        root = os.sep.join(self.__path__.split(os.sep)[:-1])
        config_path = f"{root}/config/config.cfg"
        parser = configparser.ConfigParser()
        parser.read(config_path)
        return parser[section][key]
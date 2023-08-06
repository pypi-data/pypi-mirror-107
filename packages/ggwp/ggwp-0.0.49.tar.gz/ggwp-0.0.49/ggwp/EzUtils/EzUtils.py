import pandas as pd
import numpy as np


# import pkg_resources
# path = 'EzUtils/config.cfg'
# config_path = pkg_resources.resource_filename(__name__, path)


# import configparser

# config_path  = 'config.cfg'
# parser = configparser.ConfigParser()
# parser.read(config_path)
# version = parser['default']['version']

# from ggwp.config.config import EzConfig

# version = EzConfig().__version__

class EzUtils:
    def __init__(self):
        self.__version__ = None
    
    def hello_world(self):
        print("hello world!!")

    def get_q1(self,x):
        return x.quantile(.25)

    def get_q3(self,x):
        return x.quantile(.75)
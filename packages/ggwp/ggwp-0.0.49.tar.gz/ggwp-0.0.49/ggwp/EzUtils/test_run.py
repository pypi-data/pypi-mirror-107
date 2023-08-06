import configparser

config_path  = './config.cfg'
parser = configparser.ConfigParser()
parser.read(config_path)
version = parser['default']['version']

print(version)

# print('test')

import os

print(os.getcwd())
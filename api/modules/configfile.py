#!/usr/bin/env python3

# SchoolConnect Backend
# Configuration file class
# © 2020 Johannes Kreutz.

# Include dependencies
import configparser

# Include modules
import config

# Class definition
class configfile:
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read(config.CONFIG_FILE_PATH)

    # Get config value
    def get(self, section, key):
        if key == None:
            return self.__config[section]
        return self.__config[section][key]

    # Set config value
    def set(self, section, key, value):
        self.__config[section][key] = value
        with open(config.CONFIG_FILE_PATH, "w") as f:
            self.__config.write(f)

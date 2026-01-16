'''
This file will configure application parameters used elsewhere
in the application. It will also allow us to select from multiple
configurations if we ever have a need to do so.

The config class will read the configuration values from the
settings.conf file.

Unless we add additional config parameters to settings.conf, there
should be no need to modify this file.
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Read the application configuration file
import configparser
config = configparser.ConfigParser()
config.read('settings.conf')


class Config:
    SECRET_KEY = config["DEFAULT"]["SECRET_KEY"]

    SESSION_PERMANENT = config["SESSION"]["SESSION_PERMANENT"]
    SESSION_TYPE = config["SESSION"]["SESSION_TYPE"]

    @staticmethod
    def init_app(app):
        pass

class BaseConfig(Config):
    DEBUG=True
    MYSQL_USER = config["MYSQL"]["USERNAME"]
    MYSQL_PASSWORD = config["MYSQL"]["PASSWORD"]
    MYSQL_HOST = config["MYSQL"]["HOSTNAME"]
    MYSQL_DATABASE = config["MYSQL"]["DATABASE"]
    MYSQL_CONNECTION_STRING = config["MYSQL"]["CONNECTION_STRING"]

class ProductionConfig(Config):
    DEBUG=False
    MYSQL_USER = config["MYSQL"]["USERNAME"]
    MYSQL_PASSWORD = config["MYSQL"]["PASSWORD"]
    MYSQL_HOST = config["MYSQL"]["HOSTNAME"]
    MYSQL_DATABASE = config["MYSQL"]["DATABASE"]
    MYSQL_CONNECTION_STRING = config["MYSQL"]["CONNECTION_STRING"]

class GenevaConfig(Config):
    DEBUG=True
    MYSQL_USER = config["MYSQLGENEVA"]["USERNAME"]
    MYSQL_PASSWORD = config["MYSQLGENEVA"]["PASSWORD"]
    MYSQL_HOST = config["MYSQLGENEVA"]["HOSTNAME"]
    MYSQL_DATABASE = config["MYSQLGENEVA"]["DATABASE"]
    MYSQL_CONNECTION_STRING = config["MYSQLGENEVA"]["CONNECTION_STRING"]

config = {
    'base': BaseConfig,
    'production': ProductionConfig,
    'geneva': GenevaConfig,
    'default': BaseConfig
}
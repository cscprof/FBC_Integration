'''
This file will configure application parameters used elsewhere
in the application. It will also allow us to select from multiple
configurations if we ever have a need to do so.

The config class will read the configuration values from the
settings.conf.example file.

Unless we add additional config parameters to settings.conf.example, there
should be no need to modify this file.
'''

import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))

# Read the application configuration file
config = configparser.ConfigParser()
config.read(os.path.join(basedir, 'settings.conf'))


class Config:
    SECRET_KEY = config["DEFAULT"]["SECRET_KEY"]

    SESSION_PERMANENT = config["SESSION"]["SESSION_PERMANENT"]
    SESSION_TYPE = config["SESSION"]["SESSION_TYPE"]

    @staticmethod
    def init_app(app):
        pass

class BaseConfig(Config):
    DEBUG=True
    MYSQL_USER = config["MYSQL_LOCAL"]["USERNAME"]
    MYSQL_PASSWORD = config["MYSQL_LOCAL"]["PASSWORD"]
    MYSQL_HOST = config["MYSQL_LOCAL"]["HOSTNAME"]
    MYSQL_DATABASE = config["MYSQL_LOCAL"]["DATABASE"]
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = config.get("MYSQL_PROD", "DATABASE_URI", fallback=None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
=======
    # Prefer explicit DATABASE_URI from settings, otherwise build from pieces
    _db_uri = config.get("MYSQL_LOCAL", "DATABASE_URI", fallback=None)
    if not _db_uri:
        _db_uri = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"
    SQLALCHEMY_DATABASE_URI = _db_uri
>>>>>>> main

class ProductionConfig(Config):
    DEBUG=False
    MYSQL_USER = config["MYSQL_PROD"]["USERNAME"]
    MYSQL_PASSWORD = config["MYSQL_PROD"]["PASSWORD"]
    MYSQL_HOST = config["MYSQL_PROD"]["HOSTNAME"]
    MYSQL_DATABASE = config["MYSQL_PROD"]["DATABASE"]
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = config.get("MYSQL_PROD", "DATABASE_URI", fallback=None)
=======
    _db_uri = config.get("MYSQL_PROD", "DATABASE_URI", fallback=None)
    if not _db_uri:
        _db_uri = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"
    SQLALCHEMY_DATABASE_URI = _db_uri
>>>>>>> main

class GenevaConfig(Config):
    DEBUG=True
    MYSQL_USER = config["MYSQL_LOCAL"]["USERNAME"]
    MYSQL_PASSWORD = config["MYSQL_LOCAL"]["PASSWORD"]
    MYSQL_HOST = config["MYSQL_LOCAL"]["HOSTNAME"]
    MYSQL_DATABASE = config["MYSQL_LOCAL"]["DATABASE"]
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = config.get("MYSQL_PROD", "DATABASE_URI", fallback=None)
=======
    _db_uri = config.get("MYSQL_LOCAL", "DATABASE_URI", fallback=None)
    if not _db_uri:
        _db_uri = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"
    SQLALCHEMY_DATABASE_URI = _db_uri #Resource team database connection
>>>>>>> main

config = {
    'base': BaseConfig,
    'production': ProductionConfig,
    'geneva': GenevaConfig,
    'default': BaseConfig
}
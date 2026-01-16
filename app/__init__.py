'''
This file creates the Flask application when you launch the
application with the

    python flasky.py

command from the command prompt.

Unless we add other modules to the project, there should be no
need to make changes to this file.  Changes to the file should
be coordinated with the team to ensure that the change is necessary
prior to pushing the new code to GitHub.
'''
from flask import Flask
# from flask_mysql_connector import MySQL
from config import config

# Create Flask extensions
# mysql = MySQL()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    # mysql.init_app(app)

    # Load the demo section
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    
    return app
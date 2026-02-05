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
from config  import config

# Create Flask extensions
# mysql = MySQL()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    # Load the home page section
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # Load the events page section
    from .events import events as events_blueprint
    app.register_blueprint(events_blueprint)

    # Load the resources page section
    from .resources import resources as resources_blueprint
    app.register_blueprint(resources_blueprint)

    # Load the user managent section
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    # from .signup import signup as signup_blueprint
    # app,register_blueprint(users_blueprint)

    # from .admin_panel import admin_panel as admin_panel_blueprint
    # app.register_blueprint(admin_panel_blueprint)

    # Load the profile page section
    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)
    
    return app


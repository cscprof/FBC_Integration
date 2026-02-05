from flask import current_app
from flask_login import LoginManager

login_manager = LoginManager()

login_manager.init_app(current_app)
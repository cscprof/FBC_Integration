from flask import Blueprint

users = Blueprint('users', __name__, template_folder='templates')

# signup = Blueprint('signup', __name__, template_folder='templates')
# login = Blueprint('login', __name__, template_folder='templates')
# adminpanel = Blueprint('adminpanel', __name__, template_folder='templates')

from . import views, Hashing  # Attaches routes
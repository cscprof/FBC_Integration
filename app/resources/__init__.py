from flask import Blueprint

resources = Blueprint('resources', __name__, template_folder='templates')

from . import views
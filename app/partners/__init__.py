from flask import Blueprint

partners = Blueprint('partners', __name__, template_folder='templates')

from . import views
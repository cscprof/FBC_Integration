from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

resources = Blueprint('resources', __name__, template_folder='templates')

from . import views
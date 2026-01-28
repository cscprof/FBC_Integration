from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
import os

resources = Blueprint('resources', __name__, template_folder='templates')

from . import views
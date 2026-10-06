from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
import os

tags = Blueprint('tags', __name__, template_folder='templates')

from . import views
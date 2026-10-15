from flask import Blueprint, Flask
import os

resources = Blueprint('resources', __name__, template_folder='templates')

from . import views
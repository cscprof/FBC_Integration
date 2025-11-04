from flask import Flask
from flask_cors import CORS
import os

from app.siteCalendar.routes import calendar_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.register_blueprint(calendar_bp)
CORS(app)

from app import routes
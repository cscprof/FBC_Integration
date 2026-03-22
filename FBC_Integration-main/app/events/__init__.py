from flask import Blueprint

events = Blueprint('events', __name__, template_folder='templates')


'''    
    views.py will contain all of the routes.  The routes will be in the form of:

    @events.route("/events/<page>)
    def <page>():
        # Stuff

'''    

from . import views
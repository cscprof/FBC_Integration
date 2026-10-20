from flask import Blueprint

users = Blueprint('users', __name__, template_folder='templates')



# signup = Blueprint('signup', __name__, template_folder='templates')
# login = Blueprint('login', __name__, template_folder='templates')
# adminpanel = Blueprint('adminpanel', __name__, template_folder='templates')

@users.record_once
def setup_login(state):
    app = state.app
    # Load login manager
    from .loginManager import login_manager
    login_manager.init_app(app)

    # Make role checks available in every template, e.g. {% if is_manager(current_user) %}
    from . import roles
    @app.context_processor
    def inject_role_helpers():
        return dict(
            has_role=roles.has_role,
            is_manager=roles.is_manager,
            STUDENT=roles.STUDENT,
            PARENT=roles.PARENT,
            GUARDIAN=roles.GUARDIAN,
            PARTNER=roles.PARTNER,
            ADMIN=roles.ADMIN,
            MANAGER_ROLES=roles.MANAGER_ROLES,
        )
    
from . import views  # Attaches routes
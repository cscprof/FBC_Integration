from functools import wraps
from flask import abort
from flask_login import LoginManager, current_user
from .authentication import get_account_by_id
from .roles import has_role

login_manager = LoginManager()
login_manager.login_view = 'users.login_page'

#Session Timeout info for Login_Manager, check settings.conf to configure session length (in hours)
login_manager.refresh_view = 'users.login_page'  # Name of your reauth route
login_manager.needs_refresh_message = 'Session expired. Please reauthenticate.'
login_manager.needs_refresh_message_category = 'warning'


# Creates a user account from the matching database entry for the entered user_id
@login_manager.user_loader
def load_user(user_id):
    return get_account_by_id(user_id)

#decorator to require specific role(s)
def role_required(role_id):
    """
    This is a 'Decorator Factory' which rejects a client from accessing a page unless their role_id matches the required role_id(s)
    Role ids are defined in app/roles/roles.py (STUDENT, PARENT, GUARDIAN, PARTNER, ADMIN, MANAGER_ROLES)
    Example use (single role): 
    @app.route(/route)
    @role_required(ADMIN)
    def route(
        code here
    )
    
    Example use (multiple roles):
    @app.route(/route)
    @role_required([PARTNER, ADMIN])
    def route(
        code here
    )
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not has_role(current_user, role_id):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

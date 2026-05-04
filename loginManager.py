from functools import wraps
from flask import abort
from flask_login import LoginManager, current_user
from db import get_db_connection
from app.Models.Account import Account

login_manager = LoginManager()
login_manager.login_view = 'users.home_page' 

#Session Timeout info for Login_Manager, check settings.conf to configure session length (in hours)
login_manager.refresh_view = 'login'  # Name of your reauth route
login_manager.needs_refresh_message = 'Session expired. Please reauthenticate.'
login_manager.needs_refresh_message_category = 'warning'


# Creates a user account from the mathcing database entry for the entered user_id
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
    finally:
        conn.close()
    if row:
        return Account(
            username=row['username'].capitalize() if row['username'] else '',
            email=row['email'],
            passwdHash=row['password'],
            roleID=row['role_id'],
            partnerID=row['partner_id'],
            userID=row['user_id'],
            nameFirst=row['first_name'].capitalize() if row['first_name'] else '',
            nameLast=row['last_name'].capitalize() if row['last_name'] else '',
            nameMiddle=row['middle_name'].capitalize() if row['middle_name'] else None,
            gradYear=row['graduation_year'],
            emailIsVerified=row.get('email_is_verified', 0),
            profilePicture=row.get('profile_picture', None),
        )
    return None

#decorator to require specific role(s)
def role_required(role_id):
    """
    This is a 'Decorator Factory' which rejects a client from accessing a page unless their role_id matches the required role_id(s)
    Example use (single role): 
    @app.route(/route)
    @role_required(0)
    def route(
        code here
    )
    
    Example use (multiple roles):
    @app.route(/route)
    @role_required([1, 2, 3])
    def route(
        code here
    )
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Convert single role_id to list for uniform handling
            allowed_roles = role_id if isinstance(role_id, list) else [role_id]
            if not current_user.is_authenticated or current_user.role not in allowed_roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

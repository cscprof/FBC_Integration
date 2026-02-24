from flask_login import LoginManager
from db import get_db_connection
from app.Models.Account import Account

login_manager = LoginManager()
login_manager.login_view = 'users.home_page'  # Redirect to login page if not authenticated

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
            username=row['username'],
            email=row['email'],
            passwdHash=row['password'],
            roleID=row['role_id'],
            partnerID=row['partner_id'],
            userID=row['user_id'],
            nameFirst=row['first_name'],
            nameLast=row['last_name'],
            nameMiddle=row['middle_name'],
            gradYear=row['graduation_year']
        )
    return None

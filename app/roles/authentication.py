from flask import session
from flask_login import current_user
from pymysql.cursors import DictCursor

from database import get_db_connection
from app.models.Account import Account
from .passwords import hash_check_matches


def account_from_row(row):
    """
    Creates an Account from a `users` table row.
    This is the single place an Account is built from the database, used both at login and by the login manager.
    """
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
        gradYear=row.get('graduation_year'),
        emailIsVerified=row.get('email_is_verified', False),
        profilePicture=row.get('profile_picture', None),
    )


def get_account_by_id(user_id):
    """Returns the Account for `user_id`, or None if no such user exists."""
    conn = get_db_connection()
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
    finally:
        conn.close()
    return account_from_row(row) if row else None


def authenticate_user(username, password):
    """
    Checks a username/password pair against the database.
    Returns the matching Account if the credentials are valid, otherwise None.
    Database errors are raised to the caller.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
    finally:
        conn.close()
    if row and hash_check_matches(password, row["password"]):
        return account_from_row(row)
    return None


def current_user_id(default=None):
    """
    Returns the logged-in user's id, falling back to `session['user_id']` and then `default`.
    """
    if getattr(current_user, 'is_authenticated', False):
        return current_user.id
    return session.get('user_id', default)

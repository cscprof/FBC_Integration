"""
Authentication and role checking for the application.

    loginManager.py       - Flask-Login setup, user loader and the @role_required decorator
    roles.py              - role id definitions
    authentication.py     - building Accounts from the database and login credentials
    passwords.py          - Argon2 password hashing and verification(From security team last semster)
    emailVerification.py  - email verification tokens and emails(Also from security team last semster)
"""
from .roles import STUDENT, PARENT, GUARDIAN, PARTNER, ADMIN, MANAGER_ROLES, has_role, is_manager
from .loginManager import login_manager, role_required

"""
Role ids and role-checking helpers.

Role ids match the `roles` table in the database:
    1: Student
    2: Parent
    3: Guardian
    4: Partner
    5: Admin
"""

STUDENT = 1
PARENT = 2
GUARDIAN = 3
PARTNER = 4
ADMIN = 5

# Roles allowed to manage site content (events, resources, tags, users)
MANAGER_ROLES = [PARTNER, ADMIN]


def has_role(user, roles):
    """
    Returns True if `user` is logged in and their role is in `roles`.
    `roles` may be a single role id or a list of role ids.
    """
    allowed_roles = roles if isinstance(roles, (list, tuple, set)) else [roles]
    return bool(getattr(user, "is_authenticated", False)) and getattr(user, "role", None) in allowed_roles


def is_manager(user):
    """Returns True if `user` is a Partner or Admin."""
    return has_role(user, MANAGER_ROLES)

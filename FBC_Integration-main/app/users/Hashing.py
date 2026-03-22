from argon2 import PasswordHasher, extract_parameters
from argon2.exceptions import VerifyMismatchError

"""
Argon2 hash functions.
-Argon2 was selected because it is the standard recommended by OWASP: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
-it is also memory-hard, meaning it is not susceptible to side-channel attacks. It has no known attack methods because of this, but is not quantum secure
"""

def hash_plaintext(plaintext_password):
    """
    Generates new argon2-cffi hash from plaintext_password
    """
    hasher = PasswordHasher() #no args, uses defaults which are plenty safe

    return hasher.hash(plaintext_password)


def hash_check_matches(plaintext_password, stored_hash):
    """
    Checks input password against a stored Argon2 hash.
    Automatically detects and rehashes outdated Argon2 hashes.
    """

    hasher = PasswordHasher()
        
    try:
        is_verified = hasher.verify(stored_hash, plaintext_password)
        return is_verified

    except VerifyMismatchError:
        #password did not match, alert user somehow
        return False
        





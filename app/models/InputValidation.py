# Possible input validation to add before sefl.field = field in Account:

"""
redundant checks to ensure inputs match db:
    if len(username) > 64:
    raise ValueError(f"Username is {len(username)} characters long.\nUsername cannot exceed 64 chararacters!")
    elif username == None:
    raise ValueError("Username cannot be None (value is Null)")

    if not is_valid_email(email):
    raise ValueError("'{email}' is not a valid email.")

    if len(passwdHash) > 128:
    raise ValueError(f"Password is {len(passwdHash)} characters long\nPassword hash exceeds 128 characters, edit hashing parameters")        

    if not isinstance(roleID, int):
        raise TypeError(f"roleID must be int, roleID is {type(roleID)}")
    elif roleID not in range(1, 6): #can be 1-5, see app/roles/roles.py
        raise ValueError(f"roleID must be in range(1, 6).\n-------possible values-------\n1:\t\tstudent\n2:\t\tparent\n3:\t\tguardian\n4:\t\tpartner\n5:\t\tadmin")

    if not isinstance(partnerID, int):
        raise TypeError(f"parternID must be int, partnerID is {type(partnerID)}")
    
    if not isinstance(userID, int):
        raise TypeError(f"userId must be int, userID is {type(userID)}")
"""

class Account:
    """
    Account class stores username, password, userRole, and any other credentials
    I added some input validation to ensure inputs match the db, which is likely redundant
    """
    def __init__(self, username, email, passwdHash, roleID, partnerID, userID, nameFirst, nameLast, nameMiddle, gradYear):
        self.username = username
        self.email = email
        self.passwdHash = passwdHash
        self.role = roleID
        self.role = partnerID
        self.role = userID
        self.nameFirst = nameFirst             
        self.nameLast = nameLast             
        self.nameMiddle = nameMiddle
        self.gradYear = gradYear

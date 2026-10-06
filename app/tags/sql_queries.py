from database import db_class

def get_tags():
    
    db = db_class()

    sql = """
        select * from tags
        """

    rows = db.query(sql)

    # Get all resource categories
    return rows
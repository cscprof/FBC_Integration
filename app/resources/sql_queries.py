from database import db_class


def get_resource_categories():

    db = db_class()

    sql = "SELECT * FROM resource_category"
    rows = db.query(sql)

    # Get all resource categories
    return rows


def get_resources(category_id=0):
    # Default value of 0 will return all resourcse
    
    db = db_class()

    sql = """
        select
            r.resource_id
            ,r.description
            ,r.url
            ,r.resource_category_id
            ,rc.resource_category_name
            ,r.contact_name
            ,r.contact_email
            ,r.contact_phone
            ,t.tag_name
        from
            resources r
            inner join resource_category rc on (r.resource_category_id = rc.resource_category_id)
            left join resource_tags rt on (r.resource_id = rt.resource_id)
            left join tags t on (rt.tag_id = t.tag_id)        
        """

    if category_id != 0:
        # We have a category so add the WHERE clause
        sql += f" WHERE r.resource_category_id = {category_id} "

    rows = db.query(sql)

    # Get all resource categories
    return rows

def get_tags():
    
    db = db_class()

    sql = """
        select
            t.tag_id
            ,t.tag_name
        from
            tags t
        """

    rows = db.query(sql)

    # Get all resource categories
    return rows



def get_num_categories():

    db = db_class()
    
    sql = "SELECT COUNT(*) as 'count' FROM resource_category"
    rows = db.query(sql)    

    # Get all resource categories
    return rows[0]['count']



def get_tag_list():

    db = db_class()
    
    sql = "SELECT * FROM resource_tags"
    rows = db.query(sql)

    # Get all resource categories
    return rows


def add_resource(data):
    # Add new resource
    pass


def add_tags(data, resource_id):
    # Add tags to a resource
    pass



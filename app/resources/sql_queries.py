from database import db_class


def get_resource_categories():

    db = db_class()

    sql = "SELECT * FROM resource_category"
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



def add_resource(data):
    # Add new resource

    print(f"**** {data} ****")

    db = db_class()

    # NOTE: Table Changes will require this SQL to be updated
    
    fields=''
    values=''
         

    # Add Title (required)
    f, v = add_field('title', data["title"], 'string')
    fields += f
    values += v

    # Add url (required)
    fields += ", url"
    values += f", '{data["url"]}' "

    # Add resource category id (required)
    fields += ", resource_category_id"
    rc_id = int(data["resource_category_id"])
    values += f", {rc_id} "

    # Add description
    description = None
    if data["description"]:
        fields += ", description"
        values += f", '{data["description"]}' "

    # Add contact_name
    contact_name = None
    if data["contact_name"]:
        fields += ", contact_name"
        values += f", '{data["contact_name"]}' "

    # Add contact_email
    contact_email = None
    if data["contact_email"]:
        fields += ", contact_email"
        values += f", '{data["contact_email"]}' "
    
    # Add contact_phone
    contact_phone = None
    if data["contact_phone"]:
        fields += ", contact_phone"
        values += f", '{data["contact_phone"]}' "

    # Add user_id
    user_id = None
    if data["user_id"]:
        fields += ", user_id"
        u_id = int(data["user_id"])
        values += f", {u_id} "
        
    # Build full SQL statement
    sql = f"INSERT INTO resources ( {fields[2:]} ) VALUES ( {values[2:]} )"

    # Get ID of new resource
    resource_id = db.insert(sql)

    print(sql)
    print(resource_id)

    # Attach tags to resource

    add_tags(data["selected_tags"], resource_id)


    return resource_id



def add_tags(tag_list, resource_id):
    # Add tags to a resource

    db = db_class()

    if tag_list:
        # Build full SQL statement
        for tag in tag_list:
            sql = f"INSERT INTO resource_tags ( resource_id, tag_id ) VALUES ( {resource_id }, {int(tag)} )"
            resource_tag_id = db.insert(sql)

            print(f"{resource_tag_id}: {sql}")

    return


def add_field(field_name, data, type="string"):
    # Build the field list entry and data 

    value = ''
    field = ''
    if data:
        field = f", {field_name}"

        if type == "int":
            value = f", {int(data)}"
        else:
            value = f", '{data}'"

    return field, value

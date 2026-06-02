
from . import resources as resources_blueprint
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from tagmanager import get_tags, give_tag
from . import sql_queries  as db
from loginManager import role_required


@resources_blueprint.route("/resources")
@resources_blueprint.route("/resource-directory")
def resource_directory():
    ''' 
        Get resource categories 
    '''
   
    categories_list = db.get_resource_categories()
    return render_template("resources/resourceDirectory.html", categories=categories_list)


@resources_blueprint.route("/resources/search")
def search():
    '''
        Search for resources based on category 
    '''
   
    categories_list = db.get_resource_categories()
    tag_list = db.get_tag_list()

    # Get input parameter
    category_id = request.args.get('category', default=0, type=int)    

    # If no category provided or category out of range, return to resources directory    
    if category_id == 0 or category_id > db.get_num_categories():
        render_template("resources/resourceDirectory.html", categories=categories_list)

    resources = db.get_resources(category_id) 

    # print("========================================")
    # print(categories_list)
    # print(tag_list)
    # print(resources)

    return render_template('resources/resourcesearch.html', resources=resources, categories=categories_list)

@resources_blueprint.route("/admin/resources")
@role_required([5])
def resources_admin():
    
    categories_list = db.get_resource_categories()
    resources = db.get_resources()   
    tags_list = db.get_tags()
    
    return render_template("resources/admin.html", resources=resources, categories=categories_list, tag_list=tags_list)


#HEY CHANGES WE NEED TO MAKE NEXT
##Making sure it only exists as admin
##Adding other optional fields that exist in the database (Contact Name, Contact Num, etc)
##Whatever content type is should probably be figured out
###Should capture current user id instead of just "1"
###-Owen B.


@resources_blueprint.route("/resources/upload", methods=["POST"])
@role_required([4, 5])
def upload_resource():
    
    data = {}

    # Get the required form data that the user submitted
    data['title'] = request.form.get('title', '').strip()
    data['url'] = request.form.get('url', '').strip()
    data['resource_category_id'] = request.form.get('resource_category_id', '').strip()

    # Make sure all required fields were filled out
    if not data['title'] or not data['url'] or not data['resource_category_id']:
        return redirect(url_for('resources.resources_admin'))
    
    # Get the rest of the form data
    data['description'] = request.form.get('description', '').strip()
    data['contact_name'] = request.form.get('contact_name', '').strip()
    data['contact_email'] = request.form.get('contact_email', '').strip()
    data['contact_phone'] = request.form.get('contact_phone', '').strip()

    # tags is an array of 0 or more tags
    data['selected_tags'] = request.form.getlist('tags-list[]')

    # Placeholders
    data['user_id'] = 1 # Kathleen


    print(data)

    try:
       
        resource_id = db.add_resource(data)

        if resource_id > 0 and data['selected_tags']:
            print("List has stuff")
            db.add_tags(data)
        else:
            print("No stuff in list")

        
        # Show the user their newly uploaded resource
        return redirect(url_for('resources.resources_admin'))
        
    except Exception as e:
        pass
        # If something went wrong, undo any changes and go back
        # db.session.rollback()
        return redirect(url_for('resources.resources_admin'))


@resources_blueprint.route("/resources/<int:resource_id>/edit", methods=["POST"])
@role_required([4, 5])
def edit_resource(resource_id: int):
    """Edit an existing resource."""
    try:
        resource = db.session.get(resources, resource_id)
        if not resource:
            return redirect(url_for('resources.resources_admin'))
        
        # Get the form data
        title = request.form.get('title', '').strip()
        url = request.form.get('url', '').strip()
        resource_category_id = request.form.get('resource_category_id', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        resource_tags = request.form.get('All the tags', '').strip()
        
        # Make sure all required fields were filled out
        if not title or not url or not resource_category_id:
            return redirect(url_for('resources.resources_admin'))
        
        # Update the resource
        resource.description = title
        resource.url = url
        resource.resource_category_id = int(resource_category_id)
        resource.contact_name = name if name else None
        resource.contact_email = email if email else None
        resource.contact_phone = phone if phone else None
        resource.resource_tags = resource_tags if resource_tags else None
        
        db.session.commit()
        return redirect(url_for('resources.resources_admin'))
    except Exception:
        db.session.rollback()
        return redirect(url_for('resources.resources_admin'))


@resources_blueprint.route("/resources/<int:resource_id>/delete", methods=["POST"])
@role_required([5])
def delete_resource(resource_id: int):
    """Delete a resource by ID and return to the search page."""
    try:
        resource = db.session.get(resources, resource_id)
        if resource:
            db.session.delete(resource)
            db.session.commit()
    except Exception:
        db.session.rollback()
    return redirect(url_for('resources.resources_admin'))

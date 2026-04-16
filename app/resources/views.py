
from flask import render_template, request, redirect, url_for
from sqlalchemy import select
from db import db
from .models import resources, resource_tags, resource_category, content_types
from tagmanager import get_tags, give_tag, check_tag, get_tag_id, remove_tag
from . import resources as resources_blueprint

# Use the route() decorator to tell Flask what URL should trigger the function
@resources_blueprint.route("/resources")
@resources_blueprint.route("/resource-directory")
def resource_directory():
    try:
        categories_list = db.session.execute(select(resource_category)).scalars().all()
        return render_template("resources/resourceDirectory.html", categories=categories_list)
    except:
        return render_template("resources/resourceDirectory.html", categories=[])


@resources_blueprint.route("/resourcesearch")

def resourcesearch():
    try:
        #Taken from above method for add resource button
        categories_list = db.session.execute(select(resource_category)).scalars().all()
        required_tags = []
        


        #To load resources from db
        dbselect = (
        select(
            resources.resource_id,
            resources.description,
            resources.url,
            resources.resource_category_id,
            resource_category.resource_category_name,
            resources.contact_name,
            resources.contact_email,
            resources.contact_phone,
            resources.resource_tags,
        )
        .join(
            resource_category,
            resources.resource_category_id == resource_category.resource_category_id, ))
        result = db.session.execute(dbselect).mappings().all()

        if required_tags and len(required_tags) > 0:
            filtering = []
            for row in result:
             allowed = False
             for tag in required_tags:
                if check_tag(get_tag_id(tag), row.resource_id, "Resource"):
                 allowed = True
            if allowed:
                filtering.append(row)
            result = filtering
        dblist = []    

        for row in result:
            dblist.append({
                'resource_id': row.resource_id,
                'description': row.description,
                'url': row.url,
                'resource_category_name': row.resource_category_name,
                'contact_name': row.contact_name,
                'contact_email': row.contact_email,
                'contact_phone': row.contact_phone,
            })

    except:
        categories_list = []
        # Exception creates example db entries so that those without the database can still design the webpage
        dblist = [
            {
                'resource_id': 1,
                'description': 'Geneva College Financial Aid Website',
                'url': 'https://www.geneva.edu/financial-aid/',
                'resource_category_name': 'college',
                'contact_name': 'Dean Swank',
                'contact_email': 'dswank@geneva.edu',
                'contact_phone': '18005882300'
            },
            {
                'resource_id': 2,
                'description': 'Geneva Application Process',
                'url': 'https://apply.geneva.edu/portal/applynow/tug_apply',
                'resource_category_name': 'college',
                'contact_name': None,
                'contact_email': None,
                'contact_phone': None,
            }
        ]
    
    return render_template('resources/resourcesearch.html', resources=dblist, categories=categories_list)

#HEY CHANGES WE NEED TO MAKE NEXT
##Making sure it only exists as admin
##Adding other optional fields that exist in the database (Contact Name, Contact Num, etc)
##Whatever content type is should probably be figured out
###Should capture current user id instead of just "1"
###-Owen B.
@resources_blueprint.route("/resources/upload", methods=["POST"])
def upload_resource():
    # Get the form data that the user submitted
    title = request.form.get('title', '').strip()
    url = request.form.get('url', '').strip()
    resource_category_id = request.form.get('resource_category_id', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    resource_tags = request.form.get('tags', '').strip()
    
    # Make sure all required fields were filled out
    if not title or not url or not resource_category_id:
        return redirect(url_for('resources.resource_directory'))
    
    try:
        #Guys this might be useful later so I'll leave it here but I'm changing the value to none
        #Idek what a content type is I don't think it's been implemented by anyone yet
        content_type = None
        
        # Create the new resource with all the information
        new_resource = resources(
            description=title,
            url=url,
            content_type_id=content_type,
            resource_category_id=int(resource_category_id),
            user_id=1, # Change later to be signed-in user
            contact_name=name,
            contact_email=email,
            contact_phone=phone,
            resource_tags=resource_tags,
        )
        
        # Save it to the database
        db.session.add(new_resource)
        db.session.commit()
        
        # Show the user their newly uploaded resource
        return redirect(url_for('resources.resourcesearch'))
        
    except Exception as e:
        # If something went wrong, undo any changes and go back
        db.session.rollback()
        return redirect(url_for('resources.resource_directory'))


@resources_blueprint.route("/resources/<int:resource_id>/edit", methods=["POST"])
def edit_resource(resource_id: int):
    """Edit an existing resource."""
    try:
        resource = db.session.get(resources, resource_id)
        if not resource:
            return redirect(url_for('resources.resourcesearch'))
        
        # Get the form data
        title = request.form.get('title', '').strip()
        url = request.form.get('url', '').strip()
        resource_category_id = request.form.get('resource_category_id', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        resource_tags = request.form.get('resource_tags', '').strip()
        
        # Make sure all required fields were filled out
        if not title or not url or not resource_category_id:
            return redirect(url_for('resources.resourcesearch'))
        
        element_tags = resource_tags.split(',')
        element_tags = [item.strip() for item in element_tags]

        try:
            tag_ids = [int(x) for x in element_tags]
        except ValueError:
            tag_ids = []
    
        tag_list = get_tags(resource_id, "Resource")
        for tag in tag_list:
            in_list = False
            for resource_tag in tag_ids:
                if tag == resource_tag:
                    in_list = True
                    break
            if in_list == False:
                remove_tag(tag, resource_id, "Resource")
        
        tag_list = get_tags(resource_id, "Resource")
        for resource_tag in tag_ids:
            in_list = False
            for tag in tag_list:
                if tag == resource_tag:
                    in_list = True
                    break
            if in_list == False:
                give_tag(tag, resource_id, "Resource")

        # Update the resource
        resource.description = title
        resource.url = url
        resource.resource_category_id = int(resource_category_id)
        resource.contact_name = name if name else None
        resource.contact_email = email if email else None
        resource.contact_phone = phone if phone else None
        resource.resource_tags = resource_tags if resource_tags else None
        
        db.session.commit()
        return redirect(url_for('resources.resourcesearch'))
    except Exception:
        db.session.rollback()
        return redirect(url_for('resources.resourcesearch'))


@resources_blueprint.route("/resources/<int:resource_id>/delete", methods=["POST"])
def delete_resource(resource_id: int):
    """Delete a resource by ID and return to the search page."""
    try:
        resource = db.session.get(resources, resource_id)
        if resource:
            db.session.delete(resource)
            db.session.commit()
    except Exception:
        db.session.rollback()
    return redirect(url_for('resources.resourcesearch'))

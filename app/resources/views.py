<<<<<<< HEAD
from flask import render_template
from sqlalchemy import select
from db import db
from .models import resources, resource_category
=======
from flask import render_template, request, redirect, url_for
from sqlalchemy import select
from db import db
from .models import resources, resource_category, content_types
>>>>>>> main
from . import resources as resources_blueprint

# Use the route() decorator to tell Flask what URL should trigger the function
@resources_blueprint.route("/resources")
@resources_blueprint.route("/resource-directory")
def resource_directory():
<<<<<<< HEAD
    return render_template("resources/resourceDirectory.html")
=======
    try:
        categories_list = db.session.execute(select(resource_category)).scalars().all()
        return render_template("resources/resourceDirectory.html", categories=categories_list)
    except:
        return render_template("resources/resourceDirectory.html", categories=[])
>>>>>>> main

@resources_blueprint.route("/resourcesearch.html")
def resourcesearch():
    try:
        dbselect = (
        select(
            resources.resource_id,
            resources.description,
            resources.url,
            resources.resource_category_id,
            resource_category.resource_category_name,
        )
        .join(
            resource_category,
            resources.resource_category_id == resource_category.resource_category_id ))

        dblist = db.session.execute(dbselect).mappings().all()
        return render_template('resources/resourcesearch.html', resources=dblist)
    except:
        #Exception creates example db entries so that those without the database can still design the webpage
       dblist = [
        {
            'description': 'Geneva College Financial Aid Website',
<<<<<<< HEAD
            'url': 'http://localhost:5050',
            'resource_category_name': 'college'
        },
        {
            'description': 'GENEVA COLLEGE IS THE ONLY COLLEGE AROUND APPLY NOW HERE NOWHERE ELSE',
            'url': 'http://localhost:5050',
=======
            'url': 'https://www.geneva.edu/financial-aid/',
            'resource_category_name': 'college'
        },
        {
            'description': 'Geneva Application Process',
            'url': 'https://apply.geneva.edu/portal/applynow/tug_apply',
>>>>>>> main
            'resource_category_name': 'college'
        }
       ]
    
    return render_template('resources/resourcesearch.html', resources=dblist)
<<<<<<< HEAD
=======

#HEY CHANGES WE NEED TO MAKE NEXT
##Making sure it only exists as admin
##Adding other optional fields that exist in the database (Contact Name, Contact Num, etc)
##Whatever content type is should probably be figured out
###-Owen B.
@resources_blueprint.route("/upload-resource", methods=["POST"])
def upload_resource():
    # Get the form data that the user submitted
    title = request.form.get('title', '').strip()
    url = request.form.get('url', '').strip()
    resource_category_id = request.form.get('resource_category_id', '').strip()
    
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
            user_id=1  # Change later to be signed-in user
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
>>>>>>> main

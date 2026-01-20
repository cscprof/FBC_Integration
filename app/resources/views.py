from flask import render_template
from sqlalchemy import select
#from . import db
#from .models import resources, resource_category
from . import resources as resources_blueprint

# Use the route() decorator to tell Flask what URL should trigger the function
@resources_blueprint.route("/resources")
@resources_blueprint.route("/resource-directory")
def resource_directory():
    return render_template("resources/resourceDirectory.html")

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
            'url': 'http://localhost:5050',
            'resource_category_name': 'college'
        },
        {
            'description': 'GENEVA COLLEGE IS THE ONLY COLLEGE AROUND APPLY NOW HERE NOWHERE ELSE',
            'url': 'http://localhost:5050',
            'resource_category_name': 'college'
        }
       ]
    return render_template('resources/resourcesearch.html', resources=dblist)

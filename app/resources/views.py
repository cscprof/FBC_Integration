
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from sqlalchemy import select
from db import db
from .models import resources, resource_category, content_types, partners
from . import resources as resources_blueprint
from loginManager import role_required

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
        )
        .join(
            resource_category,
            resources.resource_category_id == resource_category.resource_category_id ))

        dblist = db.session.execute(dbselect).mappings().all()

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

@resources_blueprint.route("/partners")
def partner():
    """Render partner directory cards for all visitors."""
    try:
        dbselect = (
            select(
                partners.partner_id,
                partners.name,
                partners.description,
                partners.url,
                partners.contact_name,
                partners.phone,
                partners.email,
                partners.address1,
                partners.address2,
                partners.city,
                partners.state,
                partners.zip,
            )
        )
        partnerList = db.session.execute(dbselect).mappings().all()
    except:
        partnerList = []
    return render_template("resources/partners.html", partners=partnerList)


@resources_blueprint.route("/partners/admin")
@resources_blueprint.route("/admin/partners")
@role_required([4, 5])
def partners_admin():
    """Render partner administration page for admin/partner roles."""
    try:
        dbselect = (
            select(
                partners.partner_id,
                partners.name,
                partners.description,
                partners.url,
                partners.contact_name,
                partners.phone,
                partners.email,
                partners.address1,
                partners.address2,
                partners.city,
                partners.state,
                partners.zip,
            )
        )
        partner_list = db.session.execute(dbselect).mappings().all()
    except Exception:
        partner_list = []

    return render_template("resources/partners_admin.html", partners=partner_list)

@resources_blueprint.route("/resources/admin")
@resources_blueprint.route("/admin/resources")
@role_required([4, 5])
def resources_admin():
    try:
        categories_list = db.session.execute(select(resource_category)).scalars().all()
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
            )
            .outerjoin(
                resource_category,
                resources.resource_category_id == resource_category.resource_category_id
            )
        )
        dblist = db.session.execute(dbselect).mappings().all()
    except Exception:
        categories_list = []
        dblist = []

    return render_template("resources/admin.html", resources=dblist, categories=categories_list)
#HEY CHANGES WE NEED TO MAKE NEXT
##Making sure it only exists as admin
##Adding other optional fields that exist in the database (Contact Name, Contact Num, etc)
##Whatever content type is should probably be figured out
###Should capture current user id instead of just "1"
###-Owen B.
@resources_blueprint.route("/resources/upload", methods=["POST"])
@role_required([4, 5])
def upload_resource():
    # Get the form data that the user submitted
    title = request.form.get('title', '').strip()
    url = request.form.get('url', '').strip()
    resource_category_id = request.form.get('resource_category_id', '').strip()
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    
    # Make sure all required fields were filled out
    if not title or not url or not resource_category_id:
        return redirect(url_for('resources.resources_admin'))
    
    try:
        #Guys this might be useful later so I'll leave it here, but I'm changing the value to none
        #Idek what a content type is I don't think it's been implemented by anyone yet
        content_type = None
        
        # Create the new resource with all the information
        new_resource = resources(
            description=title,
            url=url,
            content_type_id=content_type,
            resource_category_id=int(resource_category_id),
            user_id=current_user.id,
            contact_name=name,
            contact_email=email,
            contact_phone=phone,
        )
        
        # Save it to the database
        db.session.add(new_resource)
        db.session.commit()
        
        # Show the user their newly uploaded resource
        return redirect(url_for('resources.resources_admin'))
        
    except Exception as e:
        # If something went wrong, undo any changes and go back
        db.session.rollback()
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
        
        db.session.commit()
        return redirect(url_for('resources.resources_admin'))
    except Exception:
        db.session.rollback()
        return redirect(url_for('resources.resources_admin'))


@resources_blueprint.route("/resources/<int:resource_id>/delete", methods=["POST"])
@role_required([4, 5])
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


@resources_blueprint.route("/partners/upload", methods=["POST"])
@role_required([4, 5])
def upload_partner():
    """Create a partner record from admin form fields."""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    url = request.form.get('url', '').strip()
    contact_name = request.form.get('contact_name', '').strip()
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    address1 = request.form.get('address1', '').strip()
    address2 = request.form.get('address2', '').strip()
    city = request.form.get('city', '').strip()
    state = request.form.get('state', '').strip()
    zip_code = request.form.get('zip', '').strip()

    if not name:
        return redirect(url_for('resources.partners_admin'))

    try:
        new_partner = partners(
            name=name,
            description=description if description else None,
            url=url if url else None,
            contact_name=contact_name if contact_name else None,
            phone=phone if phone else None,
            email=email if email else None,
            address1=address1 if address1 else None,
            address2=address2 if address2 else None,
            city=city if city else None,
            state=state if state else None,
            zip=zip_code if zip_code else None,
        )
        db.session.add(new_partner)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('resources.partners_admin'))


@resources_blueprint.route("/partners/<int:partner_id>/edit", methods=["POST"])
@role_required([4, 5])
def edit_partner(partner_id: int):
    """Edit an existing partner by ID."""
    try:
        partner_record = db.session.get(partners, partner_id)
        if not partner_record:
            return redirect(url_for('resources.partners_admin'))

        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        url = request.form.get('url', '').strip()
        contact_name = request.form.get('contact_name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address1 = request.form.get('address1', '').strip()
        address2 = request.form.get('address2', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        zip_code = request.form.get('zip', '').strip()

        if not name:
            return redirect(url_for('resources.partners_admin'))

        partner_record.name = name
        partner_record.description = description if description else None
        partner_record.url = url if url else None
        partner_record.contact_name = contact_name if contact_name else None
        partner_record.phone = phone if phone else None
        partner_record.email = email if email else None
        partner_record.address1 = address1 if address1 else None
        partner_record.address2 = address2 if address2 else None
        partner_record.city = city if city else None
        partner_record.state = state if state else None
        partner_record.zip = zip_code if zip_code else None

        db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('resources.partners_admin'))


@resources_blueprint.route("/partners/<int:partner_id>/delete", methods=["POST"])
@role_required([4, 5])
def delete_partner(partner_id: int):
    """Delete a partner record by ID."""
    try:
        partner_record = db.session.get(partners, partner_id)
        if partner_record:
            db.session.delete(partner_record)
            db.session.commit()
    except Exception:
        db.session.rollback()

    return redirect(url_for('resources.partners_admin'))

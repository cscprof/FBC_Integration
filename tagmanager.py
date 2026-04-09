
from flask import render_template, request, redirect, url_for
from sqlalchemy import select
from db import db
from app.resources.models import resources, events, tags, users


def get_tags(element_id, element_type):
    if element_type == "Resource":
        dbselect = (select(resources.resource_tags).where(resources.resource_id == element_id))
    if element_type == "Event":
        dbselect = (select(events.event_tags).where(events.event_id == element_id))
    if element_type == "User":
        dbselect = (select(users.user_tags).where(users.user_id == element_id))

    selection = connection.execute(dbselect).fetchone()
    element_tags = selection.split(',')
    element_tags = [item.strip() for item in element_tags]

    try:
        tag_ids = [int(x) for x in element_tags]
    except ValueError:
        return
    return tag_ids

def check_tag(element_id, tag, element_type):
    tag_ids = get_tags(element_id, element_type)
    dbselect = (select(tags.tag_id).where(tags.tag == tag))
    desired_tag = connection.execute(dbselect).fetchone()
    for tag_id in tag_ids:
        if tag_id == desired_tag:
            return True
    return False

def edit_tag(tag_id: int):
    """Edit an existing tag."""
    try:
        tag = db.session.get(tags, tag_id)
        if not tag:
            return redirect(url_for('.resourcesearch'))
        
        # Get the form data
        tag = request.form.get('tag', '').strip()
        description = request.form.get('description', '').strip()
        
        
        # Make sure all required fields were filled out
        if not tag or not description:
            return redirect(url_for('resources.resourcesearch'))
        
        # Update the resource
        tags.description = description
        tags.tag = tag
        
        db.session.commit()
        return redirect(url_for('resources.resourcesearch'))
    except Exception:
        db.session.rollback()
        return redirect(url_for('resources.resourcesearch'))
    
def add_tag():
    tag = request.form.get('tag', '').strip()
    description  = request.form.get('description', '').strip()

    if not tag or not description:
        return redirect(url_for('resources.resource_directory'))
    try:
        new_tag = tags(
                tag=tag,
                description=description,
            )
        
        db.session.add(new_tag)
        db.session.commit()

        return redirect(url_for('resources.resourcesearch'))
    except Exception as e:
        # If something went wrong, undo any changes and go back
        db.session.rollback()
        return redirect(url_for('resources.resource_directory'))    
        # Save it to the database
        db.session.add(new_resource_tag)
        db.session.commit()

def give_tag(element_type):
    tag = request.form.get('tag', '').strip()
    element_id  = request.form.get('element', '').strip()


    if not tag or not element_id:
        return redirect(url_for('resources.resource_directory'))
    
    
    element_tags = get_tags(element_id, element_type)
    element_tags.append[tag]

    element_tag_string = ','.join(map(str, element_tags))
    resources.resource_tags = element_tag_string

    db.session.commit()

    return redirect(url_for('resources.resourcesearch'))
    

def remove_tag(tag_id):
    try:
        tag = db.session.get(tags, tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
    except Exception:
        db.session.rollback()
    return redirect(url_for('resources.resourcesearch'))

from flask import render_template, request, redirect, url_for
from sqlalchemy import select
from db import db
from app.resources.models import resources, events, tags, users, resource_tags, event_tags, user_tags

def get_tag_id(tag):
    dbselect = (select(tags.tag_id).where(tags.tag == tag))
    tag_id_list = connection.execute(dbselect).mappings().all()
    tag_id = tag_id_list[0]
    if tag_id != None:
        return tag_id
    else:
        return
    
def get_tags(element_id, element_type):
    if element_type == "Resource":
        dbselect = (select(resource_tags.tag_id).where(resources.resource_id == element_id))
    if element_type == "Event":
        dbselect = (select(event_tags.tag_id).where(events.event_id == element_id))
    if element_type == "User":
        dbselect = (select(user_tags.tag_id).where(users.user_id == element_id))

    selection = connection.execute(dbselect).fetchone()
    
    try:
        tag_ids = [int(x) for x in selection]
    except ValueError:
        return
    return tag_ids

def check_tag(desired_tag_id, element_id, element_type):
    tag_ids = get_tags(element_id, element_type)
    for tag_id in tag_ids:
        if tag_id == desired_tag_id:
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
    
def add_tag(tag, description):

    if not tag or not description:
        return
    try:
        new_tag = tags(
                tag=tag,
                description=description,
            )
        
        db.session.add(new_tag)
        db.session.commit()

        return
    except Exception as e:
        # If something went wrong, undo any changes and go back
        db.session.rollback()
        return   
        # Save it to the database
        db.session.add(new_resource_tag)
        db.session.commit()

def give_tag(tag_id, element_id, element_type):
    
    if not tag_id or not element_id or not element_type:
        return
    try:
        if element_type == "Resource":
            new_resource_tag = resource_tags(
                resource_id = element_id,
                tag_id = tag_id
            )
            db.session.add(new_resource_tag)
            db.session.commit()
        if element_type == "Event":
            new_event_tag = event_tags(
                event_id = element_id,
                tag_id = tag_id
            )
            db.session.add(new_event_tag)
            db.session.commit()
        if element_type == "User":
            new_user_tag = user_tags(
                resource_id = element_id,
                tag_id = tag_id
            )
            db.session.add(new_user_tag)
            db.session.commit()
        return
    except Exception as e:
        # If something went wrong, undo any changes and go back
        db.session.rollback()
        return   
        # Save it to the database
        db.session.add(new_resource_tag)
        db.session.commit()
    
    

def remove_tag(tag_id, element_id, element_type):
    try:
        if element_type == "Resource":
            tag = db.session.get(resource_tags, tag_id).where(resource_tags, resource_id = element_id)
        if element_type == "Event":
            tag = db.session.get(event_tags, tag_id).where(event_tags, event_id = element_id)
        if element_type == "User":
            tag = db.session.get(user_tags, tag_id).where(user_tags, user_id = element_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
    except Exception:
        db.session.rollback()
    return redirect(url_for('resources.resourcesearch'))
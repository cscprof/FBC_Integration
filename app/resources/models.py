from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from db import db
from datetime import datetime, timezone

#These tables may be replaced by other groups that specialize in these tables, they are just here for FK identification
#That being said they will properly build the database on init
#So maybe just tweak them so you don't have to rewrite it if you haven't yet idk
class content_types(db.Model):
    content_type_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)

class tags(db.Model):
    tag_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    tag: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)

class roles(db.Model):
    role_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    role: so.Mapped[str] = so.mapped_column(sa.Enum("Student","Parent","Guardian","Admin","Partner", name="role"), index=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)

class partners(db.Model):
    partner_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False, index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    phone: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    contact_name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    address1: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    address2: so.Mapped[str] = so.mapped_column(sa.String(128))
    city: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    state: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=False)
    zip: so.Mapped[str] = so.mapped_column(sa.String(16), nullable=False)

class users(db.Model):
    user_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False, index=True)
    middle_name: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False) #FYI this is plaintext def don't use this for the final product
    email: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    graduation_year: so.Mapped[int] =  so.mapped_column(sa.Integer, nullable=True) #This column has a typo in the original backup file
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(roles.role_id), index=True, nullable=False)
    partner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(partners.partner_id), index=True, nullable=False)

class events(db.Model):
    event_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    content_type: so.Mapped[int] = so.mapped_column(sa.ForeignKey(content_types.content_type_id), index=True, nullable=False)
    url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    posting_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    start_date: so.Mapped[datetime] = so.mapped_column(index=True)
    end_date: so.Mapped[datetime] = so.mapped_column(index=True)
    registration_deadline: so.Mapped[datetime] = so.mapped_column(index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(users.user_id), index=True, nullable=False)

class event_tags(db.Model):
    event_tag_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(events.event_id), index=True, nullable=False)
    tag_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(tags.tag_id), index=True, nullable=False)

#This table was added by us
class resource_category(db.Model):
    resource_category_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
<<<<<<< HEAD
    resource_category_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
=======
    resource_category_name: so.Mapped[str] = so.mapped_column(sa.Enum("college","mental","jobs","tutoring","activities","career", name="category"), nullable=False)
>>>>>>> main

#These tables must be implemented as written in final product
class resources(db.Model):
    resource_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    content_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(content_types.content_type_id), index=True, nullable=False)
    url: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    contact_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False, index=True)
    contact_email: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=True)
    contact_phone: so.Mapped[str] = so.mapped_column(sa.String(32), nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(users.user_id), index=True, nullable=False)
    resource_category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(resource_category.resource_category_id), index=True, nullable=False)

class resource_tags(db.Model):
    resource_tag_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    resource_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(resources.resource_id), index=True, nullable=False)
    tag_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(tags.tag_id), index=True, nullable=False)

#This table was added by us
class saved_resources(db.Model):
    saved_resource_id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(users.user_id), index=True, nullable=False)
    resource_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(resources.resource_id), index=True, nullable=False)

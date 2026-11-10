from flask import render_template
import os
import uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from database import get_db_connection
import pymysql
from pymysql import DatabaseError
from pymysql.cursors import DictCursor
from werkzeug.utils import secure_filename

from . import partners

# Authentication and role checking
from flask_login import login_user, login_required, logout_user, current_user
from ..users.loginManager import role_required
from ..users.roles import MANAGER_ROLES
from ..users.passwords import hash_plaintext, hash_check_matches
from ..users.authentication import authenticate_user
from ..users.emailVerification import send_verification_email, confirm_token

# Use the route() decorator to tell Flask what URL should trigger the function
@partners.route("/partners/apply")
def partners_apply_page():
    return render_template("partners/apply.html")

@partners.route("/partners/join")
def partners_join_page():
    return render_template("partners/join.html")

@partners.route("/partners")
def partners_page():
    return render_template("partners/index.html")

@partners.route("/partners/thankyou")
def partners_thankyou_page():
    return render_template("partners/thankyou.html")

@partners.route("/add_partner", methods=["GET", "POST"])
def add_partner():
    #Create New partner
    role_id= 4
    middle_name= None
    graduation_year = None

    if request.method == "POST":
        # get the entered values from the signup page
        name = request.form.get('organization_name', '').strip()
        description = request.form.get('description', '').strip()
        phone = request.form.get('phone_number', '').strip()
        email = request.form.get('email', '').strip()
        contact = request.form.get('contact', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        address1 = request.form.get('organizationaddress1', '').strip()
        address2 = request.form.get('organizationaddress2', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        zip = request.form.get('zip', '').strip()
 
        conn = None
        # pass the given info to the database
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO partners
                (name, description, phone, email, contact_name, address1, address2, city, state, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    name, description, phone, email, contact, address1, address2, city, state, zip
                ))

                partner_id = cursor.lastrowid

                sql_user = """
                INSERT INTO users
                (first_name, last_name, middle_name, password, email, graduation_year, username, role_id, partner_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                cursor.execute(sql_user, (
                                    name, contact, middle_name, hash_plaintext(password),
                                    email, graduation_year, username, role_id, partner_id
                                ))

                conn.commit()
                flash("Partner created!", "success")
        # error handling for an already used username
        except pymysql.err.IntegrityError:
            flash('Username taken!')
        
        # error handling for a database error
        except DatabaseError as e:
            print(f"DB Error: {e}")
            flash(f"Error: {e}", "error")
            if conn:
                conn.rollback()
            return redirect(url_for('partners.partners_apply_page'))
        finally:
            if conn:
                conn.close()
        return redirect(url_for('partners.partners_thankyou_page'))
    #ask spear if we should redirect to thankyou or user login
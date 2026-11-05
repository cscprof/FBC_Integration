from flask import render_template
import os
import uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from database import get_db_connection
from pymysql import DatabaseError
from pymysql.cursors import DictCursor
from werkzeug.utils import secure_filename

from . import partners

# Use the route() decorator to tell Flask what URL should trigger the function
@partners.route("/partners/apply")
def partners_apply_page():
    return render_template("partners/apply.html")

@partners.route("/partners")
def partners_page():
    return render_template("partners/index.html")

@partners.route("/partners/thankyou")
def partners_thankyou_page():
    return render_template("partners/thankyou.html")

@partners.route("/add_partner", methods=["GET", "POST"])
def add_partner():
    #Create New partner

    if request.method == "POST":
        # get the entered values from the signup page
        name = request.form.get('Organization', '').strip()
        description = request.form.get('Description', '').strip()
        phone = request.form.get('Phone Number', '').strip()
        email = request.form.get('email', '').strip()
        contact = request.form.get('Contact', '').strip()
        address1 = request.form.get('address1', '').strip()
        address2 = request.form.get('address2', '').strip()
        city = request.form.get('City', '').strip()
        state = request.form.get('State', '').strip()
        zip = request.form.get('Zip', '').strip()
        
        conn = None
        # pass the given info to the database
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO partners
                (name, description, phone, email, contact, address1, address2, city, state, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    name, description, phone, email, contact, address1, address2, city, state, zip
                ))
                conn.commit()
                flash("Partner created!", "success")
        # error handling for an already used username
        except pymysql.err.IntegrityError:
            flash('Username taken!')
        
        # error handling for a daatabase error
        except DatabaseError as e:
            print(f"DB Error: {e}")
            flash(f"Error: {e}", "error")
            if conn:
                conn.rollback()
            return redirect(url_for('partner.apply'))
        finally:
            if conn:
                conn.close()
        return redirect(url_for('partner.thankyou'))
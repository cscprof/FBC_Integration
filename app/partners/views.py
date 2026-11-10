import os
import uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from flask import render_template
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
    conn = get_db_connection()
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("SELECT * FROM partners")
            partners = cursor.fetchall()
            return render_template('partners/index.html', partners=partners)
    except Exception as e:
        flash(f"Error loading partners: {e}", "danger")
        return redirect(url_for('home.index'))
    finally:
        if conn:
            conn.close()
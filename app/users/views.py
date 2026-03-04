from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection
from pymysql import DatabaseError
from pymysql.cursors import DictCursor

# Hashing (create app/users/Hashing.py if missing)
from .Hashing import hash_plaintext, hash_check_matches
from . import users
# from . import signup, login, adminpanel

# For creating a user account
from flask_login import login_user, login_required, logout_user, current_user
from loginManager import role_required
from app.Models.Account import Account

# Sign Up
@users.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        #Get all userinfo from webpage, strip any whitespace, then normalize to lowercase for all except password which remains case-sensitive
        role_id = request.form.get('userRole', '').strip().lower()
        first_name = request.form.get('first_name', '').strip().lower()
        last_name = request.form.get('last_name', '').strip().lower()
        middle_name = request.form.get('middle_name', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        graduation_year = request.form.get('graduation_year', '').strip().lower()
        password = request.form.get('password', '').strip()
        passwordConfirmation = request.form.get('passwordConfirmation', '').strip()
        username = request.form.get('username', '').strip().lower()

        if password != passwordConfirmation:
            flash("Passwords do not match", "error")
            return redirect(url_for('users.signup_page'))

        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO users
                (first_name, last_name, middle_name, password, email, graduation_year, username, role_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    first_name, last_name, middle_name, hash_plaintext(password),
                    email, graduation_year, username, role_id
                ))
                conn.commit()
                flash("User created!", "success")
        except DatabaseError as e:
            print(f"DB Error: {e}")
            flash(f"Error: {e}", "error")
            if conn:
                conn.rollback()
            return redirect(url_for('users.signup_page'))
        finally:
            if conn:
                conn.close()
        return redirect(url_for('users.home_page'))

@users.route('/signup')
def signup_page():
    return render_template("/signup/signup.html")

# Login
@users.route("/login")
def home_page():
    return render_template("login/login.html")

@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect("/")

@users.route("/auth_login", methods=["GET", "POST"])
def auth_login():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password_given = request.form.get('password', '').strip()
        is_auth = False
        row = None
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor(DictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                row = cursor.fetchone()
                if row and hash_check_matches(password_given, row["password"]):
                    is_auth = True

                    # Create user from the Account class
                    # This user can then be used by the login manager anywhere in this program 
                    # Accessed by current_user.role for setting role permissions
                    user = Account(
                        username=row['username'],
                        email=row['email'],
                        passwdHash=row['password'],
                        roleID=row['role_id'],
                        partnerID=row['partner_id'],
                        userID=row['user_id'],
                        nameFirst=row['first_name'],
                        nameLast=row['last_name'],
                        nameMiddle=row['middle_name'],
                        gradYear=row['graduation_year']
                    )
                    login_user(user, remember=False)    #Makes session cookies reset whenever you leave the page, and stops them from tracking session age. 
                                                        #Server will track session age
        except DatabaseError as e:
            flash(f"DB Error: {e}", "error")
            return render_template('login/login.html', form=request.form)
        finally:
            if conn:
                conn.close()
        if is_auth:
            return redirect(url_for('home.home_page'))
            # return redirect(url_for('profile.profile', username=username))
        flash("Invalid login")
        return redirect(url_for('login.home_page'))

# Admin
@users.route("/admin/users")
@role_required(4)
def admin_panel():
    conn = get_db_connection()
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("USE flourish_bc")
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return render_template("adminpanel/index.html", users=users)
    finally:
        conn.close()

@users.route("/admin/user/<int:user_id>/edit", methods=["GET", "POST"])  # FIXED route
def edit_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor(DictCursor) as cursor:
            if request.method == "POST":
                first_name = request.form.get("first_name") or ""
                middle_name = request.form.get("middle_name") or ""
                last_name = request.form.get("last_name") or ""
                email = request.form.get("email") or ""
                graduation_year = int(request.form.get("graduation_year") or 0)
                username = request.form.get("username") or ""
                role_id = int(request.form.get("role_id") or 0)

                cursor.execute("""
                    UPDATE users SET first_name=%s, middle_name=%s, last_name=%s,
                    email=%s, graduation_year=%s, username=%s, role_id=%s
                    WHERE user_id=%s
                """, (first_name, middle_name, last_name, email, graduation_year,
                      username, role_id, user_id))
                conn.commit()
                flash("User updated!")
                return redirect(url_for("users.admin_panel"))

            cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
            user = cursor.fetchone()
    finally:
        conn.close()

    if not user:
        flash("User not found")
        return redirect(url_for("users.admin_panel"))
    return render_template("adminpanel/edit_user.html", user=user)

@users.route("/profile")
@login_required
def profile():

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                SELECT *
                FROM users
                WHERE username = %s
            """
            cursor.execute(sql, (current_user.username,))
            output = cursor.fetchall()

    except DatabaseError as e:

        flash("Database error: " + str(e), "error")
        if conn:
            conn.rollback()
        return render_template("profile/profile.html")

    finally:
        if conn:
            conn.close()

    return render_template("profile/profile.html", user=output)
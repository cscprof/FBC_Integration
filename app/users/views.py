import pymysql
import os
import uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from db import get_db_connection
from pymysql import DatabaseError
from pymysql.cursors import DictCursor
from werkzeug.utils import secure_filename

# Hashing (create app/users/Hashing.py if missing)
from .Hashing import hash_plaintext, hash_check_matches
from . import users
from .emailVerification import send_verification_email, confirm_token
# For creating a user account
from flask_login import login_user, login_required, logout_user, current_user
from loginManager import role_required
from app.Models.Account import Account

# allowed files types for user pfps
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Signup
@users.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        # get the entered values from the signup page
        role_id = request.form.get('userRole', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        middle_name = request.form.get('middle_name', '').strip()
        email = request.form.get('email', '').strip()
        graduation_year_raw = request.form.get('graduation_year', '').strip()
        # checks if the entered grad year is valid
        if not graduation_year_raw: graduation_year = None 
        else:
            try: 
                graduation_year = int(graduation_year_raw)
            except ValueError:
                flash("Graduation year must be an integer.")
                return render_template('signup/signup.html', form=request.form)
        password = request.form.get('password', '').strip()
        passwordConfirmation = request.form.get('passwordConfirmation', '').strip()
        username = request.form.get('username', '').strip().lower()

        # checks if entered password is the same if both fields
        if password != passwordConfirmation:
            flash("Passwords do not match", "error")
            return redirect(url_for('users.signup_page'))

        conn = None
        # pass the given info to the database
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
        # error handling for an already used username
        except pymysql.err.IntegrityError:
            flash('Username taken!')
        
        # error handling for a daatabase error
        except DatabaseError as e:
            print(f"DB Error: {e}")
            flash(f"Error: {e}", "error")
            if conn:
                conn.rollback()
            return redirect(url_for('users.signup_page'))
        finally:
            if conn:
                conn.close()
        return redirect(url_for('users.login_page'))

@users.route('/signup')
def signup_page():
    return render_template("/signup/signup.html")

# Login
@users.route("/login")
def login_page():
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
                        gradYear=row['graduation_year'],
                        emailIsVerified=row['email_is_verified'],
                        profilePicture=row['profile_picture'],
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
        flash("Invalid Login. Username or Password is Incorrect. Please Try Again!")
        return redirect(url_for('users.login_page'))


# new route requested by navbar: serve the more polished userAdmin.html page
@users.route("/admin/users")
@role_required([4, 5])
def admin_users():
    conn = get_db_connection()
    try:
        with conn.cursor(DictCursor) as cursor:
            cursor.execute("USE flourish_bc")
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return render_template("adminpanel/userAdmin.html", users=users)
    finally:
        conn.close()

@users.route("/admin/user/<int:user_id>/edit", methods=["GET", "POST"])  # FIXED route
def edit_user(user_id):
    conn = get_db_connection()
    # gets dats from data pass and passes it to edit_profile.html
    try:
        with conn.cursor(DictCursor) as cursor:
            if request.method == "POST":
                first_name = request.form.get("first_name") or ""
                middle_name = request.form.get("middle_name") or ""
                last_name = request.form.get("last_name") or ""
                email = request.form.get("email") or ""
                graduation_year_raw = request.form.get("graduation_year")
                if not graduation_year_raw or graduation_year_raw.strip().lower() == "none":
                    graduation_year = None
                else:
                    graduation_year = int(graduation_year_raw)

                username = request.form.get("username") or ""
                role_id = int(request.form.get("role_id") or 0)

                cursor.execute("""
                    UPDATE users SET first_name=%s, middle_name=%s, last_name=%s,
                    email=%s, graduation_year=%s, username=%s, role_id=%s
                    WHERE user_id=%s
                """, (first_name, middle_name, last_name, email, graduation_year,
                      username, role_id, user_id))
                conn.commit()
                flash("User updated!", "success")
                return redirect(url_for("users.admin_users"))

            cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
            user = cursor.fetchone()

    finally:
        conn.close()

    # error handling to for if a user does not exist
    if not user:
        flash("User not found")
        return redirect(url_for("users.admin_panel"))
    return render_template("adminpanel/edit_user.html", user=user)

@users.route("/profile")
@login_required
def profile():

    conn = None
    # allows logged in users to go to their respective profile page
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

@users.route("/profile/<username>/edit", methods=["GET", "POST"])
def edit_profile(username):

    conn = get_db_connection()
    # gets user data from database and passes 
    try:
        with conn.cursor(DictCursor) as cursor:
            if request.method == "POST":
                first_name = request.form.get("first_name") or ""
                middle_name = request.form.get("middle_name") or ""
                last_name = request.form.get("last_name") or ""
                email = request.form.get("email") or ""
                graduation_year_raw = (request.form.get("graduation_year"))
                if not graduation_year_raw or graduation_year_raw.strip().lower() == "none":
                    graduation_year = None
                else:
                    graduation_year = int(graduation_year_raw)

                # Profile picture upload
                profile_picture_path = None
                file = request.files.get("profile_picture")
                if file and file.filename and allowed_file(file.filename):
                    # current_app.static_folder is the guaranteed absolute path to /static
                    save_dir = os.path.join(
                        current_app.static_folder, "images", "profile_pictures"
                    )
                    os.makedirs(save_dir, exist_ok=True)

                    # Delete old profile picture if one exists
                    cursor.execute("SELECT profile_picture FROM users WHERE username=%s", (username,))
                    existing = cursor.fetchone()
                    if existing and existing.get("profile_picture"):
                        old_path = os.path.join(current_app.static_folder, existing["profile_picture"])
                        if os.path.isfile(old_path):
                            os.remove(old_path)

                    ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
                    unique_filename = f"{uuid.uuid4().hex}.{ext}"
                    file.save(os.path.join(save_dir, unique_filename))

                    # Must use forward slashes: url_for('static', filename=...) requires it
                    profile_picture_path = f"images/profile_pictures/{unique_filename}"

                if profile_picture_path:
                    cursor.execute("""
                        UPDATE users SET first_name=%s, middle_name=%s, last_name=%s,
                        email=%s, graduation_year=%s, profile_picture=%s
                        WHERE username=%s
                    """, (first_name, middle_name, last_name, email, graduation_year,
                          profile_picture_path, username))
                else:
                    cursor.execute("""
                        UPDATE users SET first_name=%s, middle_name=%s, last_name=%s,
                        email=%s, graduation_year=%s
                        WHERE username=%s
                    """, (first_name, middle_name, last_name, email, graduation_year,
                          username))

                conn.commit()
                flash("User updated!", "success")
                return redirect(url_for("users.profile", username=username))

            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
    finally:
        conn.close()

    if not user:
        flash("User not found")
        return redirect(url_for("profile.user_profile", username=username))
    return render_template("profile/edit_profile.html", user=user)


@users.route("/profile/<username>/change-password", methods=["GET", "POST"])
def change_password(username):

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(DictCursor) as cursor:

            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()

            if not user:
                flash("User not found.", "error")
                return redirect(url_for("profile.user_profile", username=username))

            if request.method == "POST":
                current_password  = request.form.get("current_password", "")
                new_password      = request.form.get("new_password", "")
                confirm_password  = request.form.get("confirm_password", "")

                # Verify the current password against the stored Argon2 hash
                if not hash_check_matches(current_password, user["password"]):
                    flash("Current password is incorrect.", "error")
                    return render_template("profile/change_password.html", user=user)

                if new_password != confirm_password:
                    flash("New passwords do not match.", "error")
                    return render_template("profile/change_password.html", user=user)

                if len(new_password) < 8:
                    flash("New password must be at least 8 characters.", "error")
                    return render_template("profile/change_password.html", user=user)

                new_hash = hash_plaintext(new_password)

                cursor.execute(
                    "UPDATE users SET password=%s WHERE username=%s",
                    (new_hash, username)
                )
                conn.commit()

                flash("Password changed successfully!", "success")
                return redirect(url_for("users.profile", username=username))
    except DatabaseError as e:
        flash("Database error: " + str(e), "error")
        if conn:
            conn.rollback()
        return redirect(url_for("users.profile", username=username))

    finally:
        if conn:
            conn.close()

    return render_template("profile/change_password.html", user=user)

#Email Verification Page
@users.route("/email")
@login_required
def emailVerification():
    return render_template("email/index.html")

@users.route("/email/emailSent")
def emailSent():
    return render_template("/email/emailSent.html")

@users.route("/email/verifyEmail", methods=["GET", "POST"])
def verifyEmail():
    #First confirm that the email is actually used for an account
    if request.method == "POST":
        email_exists_in_database = False
        row = None
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor(DictCursor) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (current_user.email,))
                row = cursor.fetchone()
                if row:
                    email_exists_in_database = True

        except DatabaseError as e:
            flash(f"DB Error: {e}", "error")
            return render_template('login/login.html', form=request.form)
        finally:
            if conn:
                conn.close()
        if email_exists_in_database:
                send_verification_email(current_user.email)

                return redirect("/email/emailSent")
        flash("Invalid login")
        return redirect(url_for('home.home_page'))
    
@users.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash("The confirmation link is invalid or expired.", "danger")
        return redirect(url_for("verifyEmail"))
    
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # First verify the email exists
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                flash("User not found.", "danger")
                return redirect(url_for("verifyEmail"))
                        
            user_id = user['user_id']

            # Check if already verified
            cursor.execute("SELECT email_is_verified FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            
            if result and result['email_is_verified'] == 1:
                flash("Account already verified.", "info")
            else:
                # Update the correct user
                cursor.execute("""
                    UPDATE users 
                    SET email_is_verified = 1 
                    WHERE user_id = %s
                """, (user_id,))
                conn.commit()
                flash("Your account has been verified!", "success")
                
    except DatabaseError as e:
        print(f"DB Error: {e}")
        flash(f"Error verifying email.", "error")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

    return redirect("/email/success")

@users.route("/email/success")
def email_confirmed():
    return render_template("/email/verificationSuccessful.html")

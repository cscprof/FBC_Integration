from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection
from pymysql import DatabaseError
from pymysql.cursors import DictCursor

# Hashing (create app/users/Hashing.py if missing)
from .Hashing import hash_plaintext, hash_check_matches
from . import users
# from . import signup, login, adminpanel

# Sign Up
@users.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        role_id = request.form.get('userRole', '').strip()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        middle_name = request.form.get('middle_name', '').strip()
        email = request.form.get('email', '').strip()
        graduation_year = request.form.get('graduation_year', '').strip()
        password = request.form.get('password', '').strip()
        username = first_name + last_name

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
            return render_template('signup/signup.html', form=request.form)
        finally:
            if conn:
                conn.close()
        return render_template('/login/login.html')

@users.route('/signup')
def signup_page():
    return render_template("/signup/signup.html")

# Login
@users.route("/login")
def home_page():
    return render_template("login/login.html")

@users.route("/auth_login", methods=["GET", "POST"])
def auth_login():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password_given = request.form.get('password', '').strip()
        is_auth = False
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor(DictCursor) as cursor:
                cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                row = cursor.fetchone()
                if row and hash_check_matches(password_given, row["password"]):
                    is_auth = True
        except DatabaseError as e:
            flash(f"DB Error: {e}", "error")
            return render_template('login/login.html', form=request.form)
        finally:
            if conn:
                conn.close()
        if is_auth:
            return redirect(url_for('profile.profile', username=username))
        flash("Invalid login")
        return redirect(url_for('login.home_page'))

# Admin
@users.route("/admin")
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
                return redirect(url_for("adminpanel.admin_panel"))

            cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
            user = cursor.fetchone()
    finally:
        conn.close()

    if not user:
        flash("User not found")
        return redirect(url_for("adminpanel.admin_panel"))
    return render_template("adminpanel/edit_user.html", user=user)
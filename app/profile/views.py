import os
import uuid
from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from db import get_db_connection
from pymysql import DatabaseError
from pymysql.cursors import DictCursor

from . import profile
from ..users.Hashing import hash_plaintext, hash_check_matches

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@profile.route("/profile/<username>")
def user_profile(username):

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(DictCursor) as cursor:
            sql = """
                SELECT *
                FROM users
                WHERE username = %s
            """
            cursor.execute(sql, (username,))
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


@profile.route("/profile/<username>/edit", methods=["GET", "POST"])
def edit_profile(username):

    conn = get_db_connection()
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

                # --- Profile picture upload ---
                profile_picture_path = None
                file = request.files.get("profile_picture")
                if file and file.filename and allowed_file(file.filename):
                    # current_app.static_folder is the guaranteed absolute path to /static
                    save_dir = os.path.join(
                        current_app.static_folder, "images", "profile_pictures"
                    )
                    os.makedirs(save_dir, exist_ok=True)

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
                return redirect(url_for("profile.user_profile", username=username))

            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
    finally:
        conn.close()

    if not user:
        flash("User not found")
        return redirect(url_for("profile.user_profile", username=username))
    return render_template("profile/edit_profile.html", user=user)


@profile.route("/profile/<username>/change-password", methods=["GET", "POST"])
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
                return redirect(url_for("profile.user_profile", username=username))

    except DatabaseError as e:
        flash("Database error: " + str(e), "error")
        if conn:
            conn.rollback()
        return redirect(url_for("profile.user_profile", username=username))

    finally:
        if conn:
            conn.close()

    return render_template("profile/change_password.html", user=user)
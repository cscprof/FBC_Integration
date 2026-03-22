from flask import render_template, request, redirect, url_for, flash
from db import get_db_connection
from pymysql import DatabaseError
from pymysql.cursors import DictCursor

from . import profile

# Use the route() decorator to tell Flask what URL should trigger the function
@profile.route("/profile/<username>")
def user_profile(username):

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
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
                graduation_year = int(request.form.get("graduation_year") or 0)

                cursor.execute("""
                    UPDATE users SET first_name=%s, middle_name=%s, last_name=%s,
                    email=%s, graduation_year=%s
                    WHERE username=%s
                """, (first_name, middle_name, last_name, email, graduation_year,
                      username))
                conn.commit()
                flash("User updated!")
                return redirect(url_for("profile.user_profile", username=username))

            cursor.execute("SELECT * FROM users WHERE username=%s", (username))
            user = cursor.fetchone()
    finally:
        conn.close()

    if not user:
        flash("User not found")
        return redirect(url_for("profile.user_profile", username=username))
    return render_template("profile/edit_profile.html", user=user)
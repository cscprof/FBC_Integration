from flask import render_template, flash
from db import get_db_connection
from pymysql import DatabaseError

from . import profile

# Use the route() decorator to tell Flask what URL should trigger the function
@profile.route("/profile/<username>")
def profile(username):

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
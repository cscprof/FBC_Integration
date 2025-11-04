from app import app
from flask import render_template, jsonify
from app.db import get_db_connection

@app.route('/')
def check():
    return "<h1>index</h1>"

@app.route('/add-event')
def addEvent():
    return render_template('')

@app.route('/admin-view')
def adminView():
    return render_template('')

@app.route('/rejected-events')
def rejectedEvents():
    return render_template('')

@app.route("/test-db", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, first_name, last_name FROM users")
            users = cursor.fetchall()
        conn.close()
        return jsonify(users)
    except Exception as e:
        print("Error fetching users:", e)
        return jsonify({"error": str(e)}), 500
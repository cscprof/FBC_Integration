from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql
import os

# --- Load environment variables ---
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Database Connection Info ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users", methods=["GET"])
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

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    first = data.get("first_name")
    last = data.get("last_name")

    if not first or not last:
        return jsonify({"error": "Missing first_name or last_name"}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (first_name, last_name) VALUES (%s, %s)",
                (first, last)
            )
            conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        print("Error adding user:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

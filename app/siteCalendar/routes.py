from flask import Blueprint, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.db import get_db_connection

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/display-calendar')
def calendar():
    return render_template('calendar.html')

@calendar_bp.route('/approved-events', methods=["GET"])
def get_approved_events():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT name, start_date, end_date, url, description
                FROM events 
                WHERE status='approved'
            """)
            rows = cursor.fetchall()

        conn.close()

        events = []
        for row in rows:
            events.append({
                "title": row['name'],
                "start": row['start_date'].isoformat(), 
                "end": row['end_date'].isoformat(),
                "url": row.get('url'),
                "description": row.get('description')
            })

        return jsonify(events)

    except Exception as e:
        print("Error fetching approved events:", e)
        return jsonify({"error": str(e)}), 500
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app.db import get_db_connection
from datetime import datetime
from pymysql import DatabaseError

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/add-event', methods=["GET", "POST"])
def addEvent():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        url = request.form.get('url', '').strip()
        starting_date_raw = request.form.get('starting_date', '').strip()
        ending_date_raw = request.form.get('ending_date', '').strip()
        
        if not name:
            flash("Name is required.", "error")
            return render_template('addEvent.html', form=request.form)

        try:
            starting_date = datetime.fromisoformat(starting_date_raw).date() if starting_date_raw else None
            ending_date = datetime.fromisoformat(ending_date_raw).date() if ending_date_raw else None
        except ValueError:
            flash("Dates must be in YYYY-MM-DD format.", "error")
            return render_template('addEvent.html', form=request.form)

        conn = None
        try:
            print('huh')
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO events (name, description, url, start_date, end_date, user_id, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (name, description, url or None, starting_date, ending_date, 1, 'pending'))
            conn.commit()
        except DatabaseError as e:
            print(e)
            flash("Database error: " + str(e), "error")
            if conn:
                conn.rollback()
            return render_template('addEvent.html', form=request.form)
        finally:
            if conn:
                conn.close()

        return render_template('calendar.html')

    return render_template('addEvent.html')

@calendar_bp.route('/display-calendar')
def calendar():
    return render_template('calendar.html')

@calendar_bp.route('/update_event/<int:event_id>/<string:action>')
def update_event(event_id, action):
    """Update event status to approved or rejected"""
    #Check for valid input
    if action not in ["approved", "rejected"]:
        return redirect(url_for('adminView'))  
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE events SET status = %s WHERE event_id = %s", (action, event_id))
        conn.commit()
    conn.close()

    return redirect(url_for('adminView'))

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

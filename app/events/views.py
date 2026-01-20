from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# from app.db import get_db_connection
from db import get_db_connection
from datetime import datetime
from pymysql import DatabaseError

from . import events

# ---------------------------------------------------------
#  PURE PYTHON HELPER FUNCTION — returns a list of events
# ---------------------------------------------------------
def fetch_approved_events():
    """Returns approved events as a list of dicts (NOT a Flask response)."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT name, start_date, end_date, url, description, content_type, registration_deadline
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
            "description": row.get('description'),
            "content_type": row['content_type'],
            "registration_deadline": row['registration_deadline'].isoformat() if row['registration_deadline'] else None
        })

    return events


# ---------------------------------------------------------
#  ADD EVENT
# ---------------------------------------------------------
@events.route('/add-event', methods=["GET", "POST"])
def addEvent():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        url = request.form.get('url', '').strip()
        starting_date_raw = request.form.get('starting_date', '').strip()
        ending_date_raw = request.form.get('ending_date', '').strip()
        deadline_raw = request.form.get('deadline', '').strip()

        deadline = datetime.fromisoformat(deadline_raw) if deadline_raw else None
        posting_date = datetime.now()

        if not name:
            flash("Name is required.", "error")
            return render_template('events/addEvent.html', form=request.form)

        starting_date = datetime.fromisoformat(starting_date_raw)
        ending_date = datetime.fromisoformat(ending_date_raw)

        if ending_date <= starting_date:
            flash("Ending date and time must be after the starting date and time.", "error")
            return render_template('events/addEvent.html', form=request.form)

        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO events 
                    (name, description, url, start_date, end_date, user_id, status, posting_date, registration_deadline)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    name, description, url or None, starting_date, ending_date,
                    1, 'pending', posting_date, deadline
                ))
            conn.commit()

        except DatabaseError as e:
            print(e)
            flash("Database error: " + str(e), "error")
            if conn:
                conn.rollback()
            return render_template('events/addEvent.html', form=request.form)

        finally:
            if conn:
                conn.close()

        return render_template('events/calendar.html')

    return render_template('events/addEvent.html')


# ---------------------------------------------------------
#  MAIN CALENDAR PAGE
# ---------------------------------------------------------
@events.route('/calendar')
def calendar():
    return render_template('events/calendar.html')


# ---------------------------------------------------------
#  UPDATE EVENT STATUS
# ---------------------------------------------------------
@events.route('/update_event/<int:event_id>/<string:action>')
def update_event(event_id, action):
    if action not in ["approved", "rejected"]:
        return redirect(url_for('adminView'))

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE events SET status=%s WHERE event_id=%s",
            (action, event_id)
        )
        conn.commit()
    conn.close()

    return redirect(url_for('events.adminView'))

@events.route('/admin')
def adminView():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""SELECT event_id, name, status, description, start_date, end_date FROM events ORDER BY start_date DESC""")
        rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "event_id": row["event_id"],
            "name": row["name"],
            "description": row["description"],
            "status": row["status"],
            "start": row["start_date"].isoformat(),
            "end": row["end_date"].isoformat()
        })

    return render_template('events/eventAdmin.html', events=events)


# ---------------------------------------------------------
#  API ENDPOINT — returns JSON of approved events
# ---------------------------------------------------------
@events.route('/approved-events', methods=["GET"])
def get_approved_events():
    try:
        events = fetch_approved_events()
        return jsonify(events)

    except Exception as e:
        print("Error fetching approved events:", e)
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------
#  EVENTS PAGE — renders template using Python list
# ---------------------------------------------------------
@events.route('/events')
def events():
    try:
        events = fetch_approved_events()
        return render_template('events/events.html', events=events)

    except Exception as err:
        return f"Error: {err}"
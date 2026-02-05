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
def fetch_approved_events_json():
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

def fetch_approved_events_python():
    """Returns approved events with real datetime objects (for Jinja templates)."""
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
            "start": row['start_date'],
            "end": row['end_date'],
            "description": row.get('description'),
            "url": row.get('url'),
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

        return render_template('events/confirmEvent.html', event_name=name)

    return render_template('events/addEvent.html')


@events.route('/calendar')
def calendar():
    return render_template('events/calendar.html')


@events.route('/update_event/<int:event_id>/<string:action>')
def update_event(event_id, action):
    if action not in ["approved", "cancelled"]:
        return redirect(url_for('events.adminView'))

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
        cursor.execute("""SELECT event_id, name, status, description, start_date, end_date, url FROM events ORDER BY CASE WHEN status = 'pending' THEN 0 ELSE 1 END, start_date ASC""")
        rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "event_id": row["event_id"],
            "name": row["name"],
            "description": row["description"],
            "status": row["status"],
            "start": row["start_date"],
            "end": row["end_date"],
            "url": row["url"]
        })

    return render_template('events/eventAdmin.html', events=events)


@events.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        url = request.form.get('url', '').strip() or None
        starting_date_raw = request.form.get('starting_date', '').strip()
        ending_date_raw = request.form.get('ending_date', '').strip()
        deadline_raw = request.form.get('deadline', '').strip()

        print(f"DEBUG: name={name}, url={url}")
        print(f"DEBUG: starting_date_raw={starting_date_raw}")
        print(f"DEBUG: ending_date_raw={ending_date_raw}")
        print(f"DEBUG: deadline_raw={deadline_raw}")

        if not name:
            flash('Name is required.', 'error')
            return redirect(url_for('events.edit_event', event_id=event_id))

        try:
            starting_date = datetime.fromisoformat(starting_date_raw)
            ending_date = datetime.fromisoformat(ending_date_raw)
            deadline = datetime.fromisoformat(deadline_raw) if deadline_raw else None

            print(f"DEBUG: starting_date={starting_date} (type: {type(starting_date)})")
            print(f"DEBUG: ending_date={ending_date} (type: {type(ending_date)})")
            print(f"DEBUG: ending_date > starting_date = {ending_date > starting_date}")
            print(f"DEBUG: ending_date <= starting_date = {ending_date <= starting_date}")

            if ending_date <= starting_date:
                flash('Ending date and time must be after the starting date and time.', 'error')
                return redirect(url_for('events.edit_event', event_id=event_id))

            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE events SET name=%s, description=%s, url=%s, start_date=%s, end_date=%s, registration_deadline=%s
                    WHERE event_id=%s
                """, (name, description, url, starting_date, ending_date, deadline, event_id))
            conn.commit()
            conn.close()
            print(f"DEBUG: Event {event_id} updated successfully")
            flash('Event updated successfully.', 'success')
            return redirect(url_for('events.adminView'))

        except Exception as e:
            print(f"DEBUG: Error - {e}")
            import traceback
            traceback.print_exc()
            flash('Error updating event: ' + str(e), 'error')
            return redirect(url_for('events.edit_event', event_id=event_id))

    # GET: fetch event and render form
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT event_id, name, description, url, start_date, end_date, registration_deadline FROM events WHERE event_id=%s", (event_id,))
        row = cursor.fetchone()
    conn.close()

    if not row:
        flash('Event not found.', 'error')
        return redirect(url_for('events.adminView'))

    event = {
        'event_id': row['event_id'],
        'name': row['name'],
        'description': row.get('description') or '',
        'url': row.get('url') or '',
        'start_date': row['start_date'].isoformat() if row['start_date'] else '',
        'end_date': row['end_date'].isoformat() if row['end_date'] else '',
        'registration_deadline': row['registration_deadline'].isoformat() if row['registration_deadline'] else ''
    }

    return render_template('events/editEvent.html', event=event)


@events.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM events WHERE event_id=%s", (event_id,))
        conn.commit()
        flash('Event deleted.', 'success')
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()
        flash('Error deleting event: ' + str(e), 'error')
    finally:
        if conn:
            conn.close()

    return redirect(url_for('events.adminView'))


# ---------------------------------------------------------
#  API ENDPOINT — returns JSON of approved events
# ---------------------------------------------------------
@events.route('/approved-events', methods=["GET"])
def get_approved_events():
    try:
        events = fetch_approved_events_json()
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
        events = fetch_approved_events_python()
        return render_template('events/events.html', events=events)

    except Exception as err:
        return f"Error: {err}"
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
# from app.db import get_db_connection
from db import get_db_connection
from datetime import datetime
from pymysql import DatabaseError
from loginManager import role_required

from . import events

# ---------------------------------------------------------
#  PURE PYTHON HELPER FUNCTION — returns a list of events
# ---------------------------------------------------------
def fetch_approved_events_json():
    """Returns approved events as a list of dicts (NOT a Flask response)."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT e.event_id, e.name, e.start_date, e.end_date, e.url, e.description, e.content_type, e.registration_deadline,
                   e.contact_name, e.contact_phone, e.contact_email,
                   e.event_address1, e.event_address2, e.event_city, e.event_state, e.event_postal_code,
                   ct.name as content_type_name
            FROM events e
            LEFT JOIN content_types ct ON e.content_type = ct.content_type_id
            WHERE e.status='approved'
        """)
        rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        # Get schools for this event
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT t.tag
                FROM event_tags et
                JOIN tags t ON et.tag_id = t.tag_id
                WHERE et.event_id = %s
            """, (row['event_id'],))
            school_rows = cursor.fetchall()
        conn.close()
        
        schools = [s['tag'] for s in school_rows]
        
        events.append({
            "title": row['name'],
            "start": row['start_date'].isoformat(),
            "end": row['end_date'].isoformat(),
            "url": row.get('url'),
            "description": row.get('description'),
            "tag": row.get('content_type_name') or "N/A",
            "schools": schools,
            "registration_deadline": row['registration_deadline'].isoformat() if row['registration_deadline'] else None,
            "contact_name": row.get('contact_name'),
            "contact_phone": row.get('contact_phone'),
            "contact_email": row.get('contact_email'),
            "event_address1": row.get('event_address1'),
            "event_address2": row.get('event_address2'),
            "event_city": row.get('event_city'),
            "event_state": row.get('event_state'),
            "event_postal_code": row.get('event_postal_code'),
        })

    return events

def fetch_approved_events_python():
    """Returns approved events with real datetime objects (for Jinja templates)."""
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT name, start_date, end_date, url, description,
                   contact_name, contact_phone, contact_email,
                   event_address1, event_address2, event_city, event_state, event_postal_code
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
            "contact_name": row.get('contact_name'),
            "contact_phone": row.get('contact_phone'),
            "contact_email": row.get('contact_email'),
            "event_address1": row.get('event_address1'),
            "event_address2": row.get('event_address2'),
            "event_city": row.get('event_city'),
            "event_state": row.get('event_state'),
            "event_postal_code": row.get('event_postal_code'),
        })

    return events



# ---------------------------------------------------------
#  ADD EVENT
# ---------------------------------------------------------
@events.route('/add-event', methods=["GET", "POST"])
@role_required([4, 5])
def addEvent():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            content_types = [
                ('Worship', 'Worship events'),
                ('Retreat', 'Retreat events'),
                ('Training', 'Training events'),
                ('Service', 'Service events'),
                ('Meeting', 'Meeting events')
            ]
            for name, desc in content_types:
                cursor.execute('SELECT 1 FROM content_types WHERE name = %s', (name,))
                if not cursor.fetchone():
                    cursor.execute('INSERT INTO content_types (name, description) VALUES (%s, %s)', (name, desc))
            conn.commit()
            
            cursor.execute("SELECT MIN(content_type_id) as content_type_id, name FROM content_types GROUP BY name")
            tags = cursor.fetchall()
            cursor.execute("SELECT tag_id as school_tag_id, tag as school_name FROM tags")
            school_tags = cursor.fetchall()
    finally:
        conn.close()

    if request.method == "POST":
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        url = request.form.get('url', '').strip()
        content_type_id = request.form.get('tag', '').strip()
        schools = request.form.getlist('schools')
        starting_date_raw = request.form.get('starting_date', '').strip()
        ending_date_raw = request.form.get('ending_date', '').strip()
        deadline_raw = request.form.get('deadline', '').strip()

        contact_name = request.form.get('contact_name', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()
        contact_email = request.form.get('contact_email', '').strip()
        event_address1 = request.form.get('event_address1', '').strip()
        event_address2 = request.form.get('event_address2', '').strip()
        event_city = request.form.get('event_city', '').strip()
        event_state = request.form.get('event_state', '').strip()
        event_postal_code = request.form.get('event_postal_code', '').strip()

        deadline = datetime.fromisoformat(deadline_raw) if deadline_raw else None
        posting_date = datetime.now()

        if not name:
            flash("Name is required.", "error")
            return render_template('events/addEvent.html', form=request.form, tags=tags, school_tags=school_tags)

        if not content_type_id:
            flash("Content Type is required.", "error")
            return render_template('events/addEvent.html', form=request.form, tags=tags, school_tags=school_tags)

        starting_date = datetime.fromisoformat(starting_date_raw)
        ending_date = datetime.fromisoformat(ending_date_raw)

        if ending_date <= starting_date:
            flash("Ending date and time must be after the starting date and time.", "error")
            return render_template('events/addEvent.html', form=request.form, tags=tags, school_tags=school_tags)

        # prefer authenticated user's id; fall back to session value or default user 1
        if getattr(current_user, 'is_authenticated', False):
            user_id = current_user.id
        else:
            user_id = session.get('user_id', 1)

        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO events
                    (name, description, content_type, url, start_date, end_date, user_id, status, posting_date, registration_deadline,
                     contact_name, contact_phone, contact_email,
                     event_address1, event_address2, event_city, event_state, event_postal_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    name, description, content_type_id, url or None, starting_date, ending_date,
                    user_id, 'pending', posting_date, deadline,
                    contact_name or None, contact_phone or None, contact_email or None,
                    event_address1 or None, event_address2 or None, event_city or None,
                    event_state or None, event_postal_code or None
                ))
                event_id = cursor.lastrowid
                
                # Insert school tags
                for school_id in schools:
                    cursor.execute("INSERT INTO event_tags (event_id, tag_id) VALUES (%s, %s)", (event_id, school_id))
            conn.commit()

        except DatabaseError as e:
            print(e)
            flash("Database error: " + str(e), "error")
            if conn:
                conn.rollback()
            return render_template('events/addEvent.html', form=request.form, tags=tags, school_tags=school_tags)

        finally:
            if conn:
                conn.close()

        return render_template('events/confirmEvent.html', event_name=name)

    return render_template('events/addEvent.html', tags=tags, school_tags=school_tags)


@events.route('/calendar')
def calendar():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tag FROM tags ORDER BY tag")
            schools = [row['tag'] for row in cursor.fetchall()]
    finally:
        conn.close()
    return render_template('events/calendar.html', schools=schools)


@events.route('/update_event/<int:event_id>/<string:action>')
@role_required([4, 5])
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


@events.route('/admin/events')
@role_required([4, 5])
def adminView():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT e.event_id, e.name, e.status, e.description, e.start_date, e.end_date, e.url,
                   e.registration_deadline, e.user_id,
                   e.contact_name, e.contact_phone, e.contact_email,
                   e.event_address1, e.event_address2, e.event_city, e.event_state, e.event_postal_code,
                   u.username, u.first_name, u.last_name
            FROM events e
            LEFT JOIN users u ON e.user_id = u.user_id
            ORDER BY CASE WHEN e.status = 'pending' THEN 0 ELSE 1 END, e.start_date ASC
        """)
        rows = cursor.fetchall()
    conn.close()

    today = datetime.now().date()
    current_events = []
    past_events = []
    for row in rows:
        # build a readable submitter name
        if row.get('first_name') or row.get('last_name'):
            submitted_by = f"{row.get('first_name') or ''} {row.get('last_name') or ''}".strip()
        else:
            submitted_by = row.get('username') or 'Unknown'

        event_dict = {
            "event_id": row["event_id"],
            "name": row["name"],
            "description": row.get("description"),
            "status": row.get("status"),
            "start": row.get("start_date"),
            "end": row.get("end_date"),
            "url": row.get("url"),
            "registration_deadline": row.get("registration_deadline"),
            "user_id": row.get("user_id"),
            "submitted_by": submitted_by,
            "contact_name": row.get("contact_name"),
            "contact_phone": row.get("contact_phone"),
            "contact_email": row.get("contact_email"),
            "event_address1": row.get("event_address1"),
            "event_address2": row.get("event_address2"),
            "event_city": row.get("event_city"),
            "event_state": row.get("event_state"),
            "event_postal_code": row.get("event_postal_code"),
        }

        # Split into current and past based on end date
        event_end = row.get("end_date") or row.get("start_date")
        if event_end and event_end.date() >= today:
            current_events.append(event_dict)
        else:
            past_events.append(event_dict)

    return render_template('events/eventAdmin.html', events=current_events, past_events=past_events)



@events.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@role_required([4, 5])
def edit_event(event_id):
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        url = request.form.get('url', '').strip() or None
        starting_date_raw = request.form.get('starting_date', '').strip()
        ending_date_raw = request.form.get('ending_date', '').strip()
        deadline_raw = request.form.get('deadline', '').strip()
        contact_name = request.form.get('contact_name', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()
        contact_email = request.form.get('contact_email', '').strip()
        event_address1 = request.form.get('event_address1', '').strip()
        event_address2 = request.form.get('event_address2', '').strip()
        event_city = request.form.get('event_city', '').strip()
        event_state = request.form.get('event_state', '').strip()
        event_postal_code = request.form.get('event_postal_code', '').strip()

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
                    UPDATE events SET name=%s, description=%s, url=%s, start_date=%s, end_date=%s, registration_deadline=%s,
                    contact_name=%s, contact_phone=%s, contact_email=%s,
                    event_address1=%s, event_address2=%s, event_city=%s, event_state=%s, event_postal_code=%s
                    WHERE event_id=%s
                """, (name, description, url, starting_date, ending_date, deadline,
                      contact_name or None, contact_phone or None, contact_email or None,
                      event_address1 or None, event_address2 or None, event_city or None,
                      event_state or None, event_postal_code or None, event_id))
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
        cursor.execute("""SELECT event_id, name, description, url, start_date, end_date, registration_deadline,
                          contact_name, contact_phone, contact_email,
                          event_address1, event_address2, event_city, event_state, event_postal_code
                       FROM events WHERE event_id=%s""", (event_id,))
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
        'registration_deadline': row['registration_deadline'].isoformat() if row['registration_deadline'] else '',
        'contact_name': row.get('contact_name') or '',
        'contact_phone': row.get('contact_phone') or '',
        'contact_email': row.get('contact_email') or '',
        'event_address1': row.get('event_address1') or '',
        'event_address2': row.get('event_address2') or '',
        'event_city': row.get('event_city') or '',
        'event_state': row.get('event_state') or '',
        'event_postal_code': row.get('event_postal_code') or '',
    }

    return render_template('events/editEvent.html', event=event)


@events.route('/delete_event/<int:event_id>', methods=['POST'])
@role_required([4, 5])
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
        today = datetime.now().date()

        upcoming_events = []
        past_events = []
        for event in events:
            event_end = event.get('end') or event.get('start')
            if event_end.date() >= today:
                upcoming_events.append(event)
            else:
                past_events.append(event)

        upcoming_events.sort(key=lambda ev: ev['start'])
        past_events.sort(key=lambda ev: ev['start'], reverse=True)

        return render_template(
            'events/events.html',
            upcoming_events=upcoming_events,
            past_events=past_events
        )

    except Exception as err:
        return f"Error: {err}"
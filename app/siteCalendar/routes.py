from flask import Blueprint, render_template, redirect, url_for
from app.db import get_db_connection


calendar_bp = Blueprint('calendar', __name__)

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
from flask import Flask, render_template
import pymysql
from pymysql.cursors import DictCursor
from config import db_config

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as err:
        return f"Error {err}"

@app.route('/admin')
def admin():
    cursor = None
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor(DictCursor)

        cursor.execute("SELECT id, name, description, start_date, end_date, url, status FROM events")
        events = cursor.fetchall()

        return render_template('adminview.html', events=events)
    except Exception as err:
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/events')
def events():
    cursor = None
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()

        return render_template('events.html', events=events)
    except Exception as err:
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if conn: 
            conn.close()

@app.route('/calendar')
def calendar():
    try:
        return render_template('cal.html')
    except Exception as err:
        return f"Error {err}"
    
@app.route('/resource-directory')
def resources():
    try:
        return render_template('resourceDirectory.html')
    except Exception as err:
        return f"Error {err}"

@app.route('/signup')
def signup():
    try:
        return render_template('signup.html')
    except Exception as err:
        return f"Error {err}"
    
@app.route('/login')
def login():
    try:
        return render_template('login.html')
    except Exception as err:
        return f"Error {err}"
    
@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as err:
        return f"Error {err}"

@app.route('/jobs')
def jobs():
    try:
        return render_template('jobs.html')
    except Exception as err:
        return f"Error {err}"

@app.route('/contact')
def contact():
    try:
        return render_template('contact.html')
    except Exception as err:
        return f"Error {err}"
    
@app.route('/add-event')
def addEvent():
    try:
        return render_template('addevent.html')
    except Exception as err:
        return f"Error {err}"
    
# will get rid of this and replace the calendar with new working one
#@app.route('/calendar-test')
#def testCalendar():
#    try:
#        return render_template('cal.html')
#    except Exception as err:
#        return f"Error {err}"

if __name__ == '__main__':
    app.run(debug=True)
    
from flask import redirect, url_for

@app.route('/update_event/<int:id>/<action>')
def update_event(id, action):
    cursor = None
    conn = None
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET status=%s WHERE id=%s", (action, id))
        conn.commit()
        return redirect(url_for('admin'))
    except Exception as err:
        return f"Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


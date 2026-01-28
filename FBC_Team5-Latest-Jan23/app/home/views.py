from flask import render_template

from . import home

# Use the route() decorator to tell Flask what URL should trigger the function
@home.route("/")
def home_page():
    return render_template("home/index.html")
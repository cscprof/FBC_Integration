from flask import render_template

from . import resources

# Use the route() decorator to tell Flask what URL should trigger the function
@resources.route("/resource-directory")
def home_page():
    return render_template("resources/resourceDirectory.html")
from flask import render_template

from . import resources

# Use the route() decorator to tell Flask what URL should trigger the function
@resources.route("/resources")
@resources.route("/resource-directory")
def resource_directory():
    return render_template("resources/resourceDirectory.html")
from . import home

# Use the route() decorator to tell Flask what URL should trigger the function
@home.route("/")
def hello_world():
    return "<p>This is the home blueprint implementation</p>"
from flask import render_template

from . import partners

# Use the route() decorator to tell Flask what URL should trigger the function
@partners.route("/partners/apply")
def partners_apply_page():
    return render_template("partners/apply.html")

@partners.route("/partners")
def partners_page():
    return render_template("partners/index.html")
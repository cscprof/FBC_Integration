from flask import render_template

from . import partners

@partners.route("/partners")
def partners_page():
    return render_template("partners/index.html")
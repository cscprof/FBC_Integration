from . import tags as tags_blueprint
from flask import render_template
from . import sql_queries as db


@tags_blueprint.route("/tags")
def tag_display():

    tags = db.get_tags()
    return render_template("tags/tagDirectory.html", tags=tags)


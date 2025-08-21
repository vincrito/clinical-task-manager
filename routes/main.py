from flask import Blueprint, render_template  # Blueprint = modular routes, render_template = HTML pages

bp = Blueprint("main", __name__)  # create a blueprint called "main"

@bp.get("/")                      # define a route at the root URL ("/"), method = GET
def index():
    return render_template("index.html")  # render the index.html template

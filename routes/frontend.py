from flask import Blueprint
from flask import send_from_directory
from flask import current_app as app

import os


frontend = Blueprint("frontend", __name__)


@frontend.route("/", defaults={"path": ""})
@frontend.route("/<path:path>")
def homepage(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

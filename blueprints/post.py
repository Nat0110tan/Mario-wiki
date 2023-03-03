from flask import *

bp = Blueprint("post", __name__, url_prefix="/post")

@bp.route("/")
def post():
    return render_template("wiki-post.html")
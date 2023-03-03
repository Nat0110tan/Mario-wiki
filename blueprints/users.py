from flask import *

bp = Blueprint("users", __name__, url_prefix="/users")
@bp.route("/")
def users():
    return render_template("base.html")
from flask import *

bp = Blueprint("base", __name__, url_prefix="/base")
@bp.route("/")
def base():
    return render_template("base.html")

@bp.route("/r")
def base_r():
    return render_template("base_rightbar.html")

@bp.route("/l")
def base_l():
    return render_template("base_leftbar.html")


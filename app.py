from flask import *
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import random
import string
# from html_sanitizer import *

from authlib.integrations.flask_client import OAuth
import db
# from models import UserModel [import models from the models.py file]
app = Flask(__name__)
app.secret_key = env['APP_SECRET_KEY'] # auth


from blueprints.home import bp as home_bp
from blueprints.search import bp as search_bp
from blueprints.profile import bp as profile_bp
from blueprints.base import bp as base_bp

from blueprints.characters import bp as characters_bp
from blueprints.games import bp as games_bp
from blueprints.content import bp as content_bp
from blueprints.login import bp as login_bp
from blueprints.community import bp as community_bp
from blueprints.post import bp as post_bp
from blueprints.create_post import bp as create_post_bp
from blueprints.users import bp as users_bp


app.register_blueprint(home_bp)
app.register_blueprint(search_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(base_bp)
app.register_blueprint(characters_bp)
app.register_blueprint(games_bp)
app.register_blueprint(content_bp)
app.register_blueprint(login_bp)
app.register_blueprint(community_bp)
app.register_blueprint(post_bp)
app.register_blueprint(create_post_bp)
app.register_blueprint(users_bp)


# Startup
with app.app_context():
    print("Ensuring DB is set up!")
    db.setup()

@app.route("/base_r")
def base_r():
    return render_template("base_rightbar.html")

## AUTH
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url="URL"
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    print(token)
    session["user"] = token
    make_user() # potentially add new user to db
    return redirect("/") # Redirects to home page

@app.route("/logout")
def logout():
    session.clear() # clear python dictionary
    return redirect( # build redirect using flask
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": request.url_root, # gets home page, would use url_for() except only seems to gets page suffix when used with blueprint pages 
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

def make_user():
    user_id = session["user"]["userinfo"]["sub"]
    username = session["user"]["userinfo"]["nickname"]
    if not db.get_user_by_id(user_id):
        if db.get_user_by_username(username):
            username.join(random.choices(string.ascii_letters, k=7))
        db.add_user(user_id, username)

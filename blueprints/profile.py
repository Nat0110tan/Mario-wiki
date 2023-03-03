# from werkzeug.utils import secure_filename
from flask import *
import db, boto3,random
import utils
from os import environ as env
# from utils import sanitizer

s3 = boto3.client('s3',
                  aws_access_key_id=env['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=env['AWS_SECRET_ACCESS_KEY'])

bp = Blueprint("profile", __name__, url_prefix="/profile")

@bp.route("/", methods=["GET", "POST"])
def profile():
    if session.get("user"):
        if request.method == "POST":
            return update()
        user_id = session["user"]["userinfo"]["sub"]
        user = db.get_user_by_id(user_id)
        user_img = user[0]['photo_url']
        user_bio = user[0]['bio']
        user_name = session["user"]["userinfo"]["nickname"]
        user_post = 2
        user_fan = 3

        page = request.args.get('page')
        if page == None:
            page = 0
        else:
            page = int(page)

        recent_posts = db.get_recent_posts_by_user(user_name, type="POST", page=page)
        for post in recent_posts:
            post[3] = utils.get_elapsed_time(post[3]) # convert timestamp to elapsed time

        recent_discussions = db.get_recent_discussion_by_user_id(user_id,type="DISCUSSION")
        for discussion in recent_discussions:
            discussion[3] = utils.get_elapsed_time(discussion[3]) # convert timestamp to elapsed time

        page_count = utils.get_total_pages(db.get_post_count(type="DISCUSSION")[0])

        data = {
            "user_img": user_img,
            "user_bio": user_bio,
            "user_name": user_name,
            "user_post": user_post,
            "user_fan": user_fan,
            "recent_posts": recent_posts,
            "recent_discussions": recent_discussions,
            "page_count": page_count,
            "page": page
        }
        return render_template("profile.html", data=data,post_url=request.url_root + "categories/")
    else:
        return redirect("/")

def update():
    content = request.form.get("content")
    user_id = session["user"]["userinfo"]["sub"]
    bio = utils.sanitizer.sanitize(content)
    db.update_user_bio(user_id, bio)
    return redirect("/profile")
 


@bp.route('/upload', methods=['POST'])
def upload():
  file = request.files['photo']
  user_id = session["user"]["userinfo"]["sub"]
  filename = f"{user_id}/profile_photo"
  s3.upload_fileobj(file, BUCKETNAME, filename)
  photo_url = PHOTO_URL
  db.update_user_img(photo_url,user_id)
  return '', 204

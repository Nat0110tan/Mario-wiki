from flask import *
import db
import utils
# from utils import sanitizer

bp = Blueprint("create_post", __name__, url_prefix="/post")
@bp.route("/create", methods=["POST", "GET"])
def create_post():
    if request.method == 'POST':
        return add_post()
    elif session.get("user") != None:
        categories = db.get_category_titles()
        data = {
            "categories": categories
        }
        return render_template("create_post.html", data=data)
    else:
        return redirect("/login")

def add_post():
    if session.get("user") != None:
        data = request.form
        # print(request.form)
        title = data.get("title")
        content = data.get("content")
        # Sanitize the content
        content = utils.sanitizer.sanitize(content)
        category = data.get("category")
        user_id = session["user"]["userinfo"]["sub"]
        db.add_post(title, content, category, user_id, "POST")
    return redirect("/")

@bp.route("/detail/<post_id>", methods=["POST", "GET"])
def detail(post_id):
    post = db.get_post_by_id(post_id)
    post_data = {
        "post_title": post[7],
        "post_content": post[2],
        "post_category":post[3].lower(),
        "post_time":post[4].strftime("%m/%d/%Y, %H:%M:%S"),
        "post_id":post_id,
    }

    category = db.get_category_by_name(post[3])
    category_data={
        "category_description": category[1],
        "category_icon" : category[2]
    }

    author_id = post[1]
    author = db.get_user_by_id(author_id)[0]
    author_post = db.get_post_count_by_user(author_id)
    author_data = {
            "author_img": author[2],
            "author_bio": author[3],
            "author_name": author[1],
            "author_fan": 3,##add ollowers if we decide we want to do it
            "author_post":author_post[0],
        }
    
    comments = db.get_comments_by_post_id(post_id)
    if comments:
        for comment in comments:
            comment_user= db.get_user_by_id(comment[1])[0]
            comment[1]=comment_user
            comment[4] = utils.get_elapsed_time(comment[4])

    if session.get("user") != None:
        if request.method == "POST":
            return create_comment(post_id)
        else:
            user = session["user"]["userinfo"]["nickname"]
            return render_template('details.html', comments=comments,post_data=post_data, author_data=author_data, user=user, category_data=category_data)
    else:   
        return render_template('details.html', comments=comments,post_data=post_data, author_data=author_data, category_data=category_data)


def create_comment(post_id):
    content = request.form.get("content")
    print(content)
    content = utils.sanitizer.sanitize(content)
    user_id = session["user"]["userinfo"]["sub"]
    db.add_comment(user_id, post_id, content)
    return redirect(f"/post/detail/{post_id}")



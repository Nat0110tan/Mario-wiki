from flask import *
import db
import utils

bp = Blueprint("community", __name__, url_prefix="/community")
@bp.route("/")
def community():
    categories = db.get_category_titles()
    recent_posts = db.get_recent_posts(type="DISCUSSION")

    games_category_count = db.get_post_count_by_category(category="Games", type="DISCUSSION")[0]
    recent_games = db.get_recent_posts_by_category(category="Games", type="DISCUSSION")[0]
    recent_games[3] = utils.get_elapsed_time(recent_games[3])
    
    character_category_count = db.get_post_count_by_category(category="Characters", type="DISCUSSION")[0]
    recent_character = db.get_recent_posts_by_category(category="Characters", type="DISCUSSION")[0]
    recent_character[3] = utils.get_elapsed_time(recent_character[3])
    
    content_category_count = db.get_post_count_by_category(category="Content", type="DISCUSSION")[0]
    recent_content = db.get_recent_posts_by_category(category="Content", type="DISCUSSION")[0]
    recent_content[3] = utils.get_elapsed_time(recent_content[3])

    page = request.args.get('page')
    if page == None:
        page = 0
    else:
        page = int(page)
    recent_posts = db.get_recent_posts(type="DISCUSSION", page=page)
    
        # parser = utils.MyHTMLParser()
        # parser.feed(post[1])
        # raw_text = parser.rawText

        # db.set_raw_text(post[8], raw_text)
    
    page_count = utils.get_total_pages(db.get_post_count(type="DISCUSSION")[0])

    for recent_post in recent_posts:
        print(recent_post[6])

    if session.get("user"):
        user_id = session["user"]["userinfo"]["sub"]
        user = db.get_user_by_id(user_id)
        user_img = user[0]['photo_url']
    else: 
        user_img = None

    data = {
        "games_category_count": games_category_count,
        "character_category_count": character_category_count,
        "content_category_count": content_category_count,
        "recent_games": recent_games,
        "recent_character": recent_character,
        "recent_content": recent_content,
        "categories": categories,
        "recent_posts": recent_posts,
        "page_count": page_count,
        "page": page,
        "user_img": user_img
    }
        
    return render_template("community_feed.html", data=data)

@bp.route("/discussion/create", methods=["POST"])
def add_discussion():
    if session.get("user") != None:
        data = request.form
        #print(request.form)
        title = data.get("title")
        content = data.get("content")
        # Sanitize the content
        content = utils.sanitizer.sanitize(content)
        category = data.get("category")
        user_id = session["user"]["userinfo"]["sub"]
        db.add_post(title, content, category, user_id, "DISCUSSION")
    return redirect("/community")
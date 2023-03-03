from flask import *
import db
import utils

bp = Blueprint("characters", __name__, url_prefix="/categories/characters")

@bp.route("/")
def characters():
  args = request.args

  if args:
    title = args['page']
    database = db.get_post_by_title(title=title)

    content = utils.add_class_to_imgs(content)

    parser = utils.MyHTMLParser()
    parser.feed(content)
    rawText = parser.rawText # The raw text from the quill object.

    data = {
      "title": title,
      "content": content,
      "category": category,
      "author": author,
      "headers": headers
    }
    return render_template("wiki-post.html", data=data)
  
  else:
    category = "Characters"
    # This list would be generated from the database using a query string such as 
    #   'select * from sub-categories-table where category=characters order by likes order by name limit 4'
    # Or something similar. This is just temporary.
    trending = [
      {"name": "Luigi", "category": "characters", "img": "https://mariopartylegacy.com/wp-content/uploads/2011/08/luigiprofile-275x275.png"},
      {"name": "Mario", "category": "characters", "img": "https://mariopartylegacy.com/wp-content/uploads/2011/08/marioprofile-275x275.png"},
      {"name": "Wario", "category": "characters", "img": "https://mariopartylegacy.com/wp-content/uploads/2011/08/warioprofile-275x275.png"},
      {"name": "Yoshi", "category": "characters", "img": "https://mariopartylegacy.com/wp-content/uploads/2011/08/yoshiprofile-275x275.png"}
    ]

    data = {
      "category": category,
      "trending": trending
    }
    return render_template("categories.html", data=data)

@bp.route("/heroes")
def heroes():
  parent_category = "Characters"
  category = "Hero Characters"


  data = {
    "category": category,
    "trending": trending
  }
  return render_template("categories.html", data=data)

@bp.route("/enemies")
def enemies():
  category = "Enemy Characters"

  trending = [
    {"name": "Wario", "category": "characters", "img": "https://mariopartylegacy.com/wp-content/uploads/2011/08/warioprofile-275x275.png"},
    {"name": "Bowser", "category": "characters", "img": "https://mario.wiki.gallery/images/7/7d/MSOGT_Bowser.png"}
  ]

  return render_template("categories.html", data=data)

@bp.route("/species")
def species():
  category = "Character Species"

  trending = [
    {"name": "Blooper", "category": "characters", "img": "https://mario.wiki.gallery/images/thumb/b/b5/Blooper_-_MarioPartyStarRush.png/400px-Blooper_-_MarioPartyStarRush.png"},
    {"name": "Bob-omb", "category": "characters", "img": "https://mario.wiki.gallery/images/thumb/9/9e/Bobomb_-_MarioPartyStarRush.png/400px-Bobomb_-_MarioPartyStarRush.png"},
    {"name": "Koopa", "category": "characters", "img": "https://mario.wiki.gallery/images/thumb/5/5c/SuperMarioParty_KoopaTroopa.png/398px-SuperMarioParty_KoopaTroopa.png"}
  ]

  return render_template("categories.html", data=data)
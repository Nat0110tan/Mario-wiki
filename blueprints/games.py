from flask import *
import db
import utils

bp = Blueprint("games", __name__, url_prefix="/categories/games")

@bp.route("/")
def games():
  args = request.args

  if args:
    title = args['page']
    database = db.get_post_by_title(title=title)

    content = database[1]
    headers = utils.get_list_of_headers(content)
    content = headers[0]
    headers = headers[1]

    title = database[0]
    category = database[2]
    author = database[3]

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
    category = "Games"
    # This list would be generated from the database using a query string such as 
    #   'select * from sub-categories-table where category=games order by likes order by name limit 4'
    # Or something similar. This is just temporary.
    trending = [
      {"name": "Super Mario Bros. 3", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/3/31/SMB3_Boxart.png/500px-SMB3_Boxart.png"},
      {"name": "Mario Party 8", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/7/7e/MP8Box.png/500px-MP8Box.png"},
      {"name": "Super Mario World", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/d/da/Super_Mario_World_Box.png/600px-Super_Mario_World_Box.png"},
      {"name": "Mario Kart 8 Deluxe", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/9/9b/MK8_Deluxe_-_Box_NA.png/500px-MK8_Deluxe_-_Box_NA.png"}
    ]

    data = {
      "category": category,
      "trending": trending
    }
    return render_template("categories.html", data=data)

@bp.route("/super_mario_bros")
def super_mario_bros():
  category = "Super Mario Bros Series"
  
  trending = [
    {"name": "Super Mario Bros. 2", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/e/ea/SMB2_Boxart.png/500px-SMB2_Boxart.png"},
    {"name": "Super Mario Bros. 3", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/3/31/SMB3_Boxart.png/500px-SMB3_Boxart.png"},
    {"name": "Super Mario World", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/d/da/Super_Mario_World_Box.png/600px-Super_Mario_World_Box.png"},
    {"name": "New Super Mario Bros. U Deluxe", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/8/8b/NSMBU_Deluxe_Boxart.jpg/500px-NSMBU_Deluxe_Boxart.jpg"}
  ]

  data = {
    "category": category,
    "trending": trending
  }
  return render_template("categories.html", data=data)

@bp.route("/mario_kart")
def mario_kart():
  category = "Mario Kart Series"

  trending = [
    {"name": "Mario Kart 8 Deluxe", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/9/9b/MK8_Deluxe_-_Box_NA.png/500px-MK8_Deluxe_-_Box_NA.png"},
    {"name": "Mario Kart Wii", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/2/29/Mkwii.jpg/540px-Mkwii.jpg"},
    {"name": "Mario Kart 64", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/5/5f/MK64_Cover.png/600px-MK64_Cover.png"},
    {"name": "Super Mario Kart", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/8/82/Super_Mario_Kart_NA_box_art.png/500px-Super_Mario_Kart_NA_box_art.png"}
  ]

  data = {
    "category": category,
    "trending": trending
  }
  return render_template("categories.html", data=data)

@bp.route("/mario_party")
def mario_party():
  category = "Mario Party Series"

  trending = [
    {"name": "Mario Party 8", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/7/7e/MP8Box.png/500px-MP8Box.png"},
    {"name": "Mario Party", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/1/1f/MP1_Cover.png/500px-MP1_Cover.png"},
    {"name": "Super Mario Party", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/b/b6/SMP_Boxart.png/500px-SMP_Boxart.png"},
    {"name": "Mario Party Superstars", "category": "games", "img": "https://mario.wiki.gallery/images/thumb/5/5a/Mario_Party_Superstars_North_American_box_art.jpg/500px-Mario_Party_Superstars_North_American_box_art.jpg"}
  ]

  data = {
    "category": category,
    "trending": trending
  }
  return render_template("categories.html", data=data)
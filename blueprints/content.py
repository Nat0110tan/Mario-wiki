from flask import *
import db
import utils

bp = Blueprint("content", __name__, url_prefix="/categories/content")

@bp.route("/")
def content():
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

    return render_template("wiki-post.html", data=data)
  
  else:
    # This list would be generated from the database using a query string such as 
    #   'select * from sub-categories-table where category=content order by likes order by name limit 4'
    # Or something similar. This is just temporary.
    category = "Content"
    trending = [
      {"name": "Bowser's Castle", "category": "content", "img": "https://mario.wiki.gallery/images/3/3a/SM3DL-_Bowser%27s_Castle_Intro.png"},
      {"name": "Ghost Houses", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/b/b0/NSMBW_Ghost_House_Screenshot.png/240px-NSMBW_Ghost_House_Screenshot.png"},
      {"name": "Rainbow Road", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/7/79/MK8-Course-RainbowRoad.png/660px-MK8-Course-RainbowRoad.png"},
      {"name": "Yoshi's Cabana", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/9/91/YoshisCabana.png/500px-YoshisCabana.png"}
    ]


    return render_template("categories.html", data=data)

@bp.route("/locations")
def locations():
  category = "Locations"

  # This list would be generated from the database using a query string such as 
  #   'select * from sub-categories-table where category=content order by likes order by name limit 4'
  # Or something similar. This is just temporary.
  trending = [
    {"name": "Bowser's Castle", "category": "content", "img": "https://mario.wiki.gallery/images/3/3a/SM3DL-_Bowser%27s_Castle_Intro.png"},
    {"name": "Ghost Houses", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/b/b0/NSMBW_Ghost_House_Screenshot.png/240px-NSMBW_Ghost_House_Screenshot.png"},
    {"name": "Rainbow Road", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/7/79/MK8-Course-RainbowRoad.png/660px-MK8-Course-RainbowRoad.png"},
    {"name": "Yoshi's Cabana", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/9/91/YoshisCabana.png/500px-YoshisCabana.png"}
  ]

  return render_template("categories.html", data=data)

@bp.route("/items")
def items():
  category = "Items"

  # This list would be generated from the database using a query string such as 
  #   'select * from sub-categories-table where category=content order by likes order by name limit 4'
  # Or something similar. This is just temporary.
  trending = [
    {"name": "1-Up Mushroom", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/b/b4/1-Up_Mushroom_Artwork_-_Super_Mario_3D_World.png/400px-1-Up_Mushroom_Artwork_-_Super_Mario_3D_World.png"},
    {"name": "Cape Feather", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/b/bf/MK8_Deluxe_Art_-_Cape_Feather.png/350px-MK8_Deluxe_Art_-_Cape_Feather.png"},
    {"name": "Crazy Eight", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/7/71/Crazy8MK8.png/300px-Crazy8MK8.png"},
    {"name": "Star Coin", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/f/f7/NSMBU_Starcoin_Artwork.png/400px-NSMBU_Starcoin_Artwork.png"}
  ]



  return render_template("categories.html", data=data)

@bp.route("/karts")
def karts():
  category = "Karts"

  # This list would be generated from the database using a query string such as 
  #   'select * from sub-categories-table where category=content order by likes order by name limit 4'
  # Or something similar. This is just temporary.
  trending = [
    {"name": "Standard Kart", "category": "content", "img": "https://mario.wiki.gallery/images/0/05/StandardKartBodyMK8.png"},
    {"name": "Yoshi Bike", "category": "content", "img": "https://mario.wiki.gallery/images/6/62/YoshiBikeBodyMK8.png"},
    {"name": "Blue Falcon", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/7/7d/BlueFalcon-BabyMario.png/200px-BlueFalcon-BabyMario.png"},
    {"name": "Mini Beast", "category": "content", "img": "https://mario.wiki.gallery/images/thumb/2/2b/MiniBeast-DryBones.png/200px-MiniBeast-DryBones.png"}
  ]
  return render_template("categories.html", data=data)
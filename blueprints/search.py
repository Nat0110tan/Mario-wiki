from flask import *
import db, utils

bp = Blueprint("search", __name__, url_prefix="/search")
@bp.route("/", methods=["GET"])
def get_search():
    return render_template("search.html", data=None)

@bp.route("/results", methods=["GET"])
def search_results():
    page = int(request.args.get('page', '0'))
    # page = int(page)
    query = request.args.get('search_query', '')
    post_type = request.args.get('post_type', '')
    if post_type:
        search_results = db.search_post_type_full_text_content(query, post_type, page=page)
    else:
        search_results = db.search_full_text_content(query, page=page)
    data = []
    for result in search_results:
        cur_entry = {
            "id": result[0],
            "user_id": result[1],
            "content": result[2],
            "category": result[3],
            "post_date": utils.get_elapsed_time(result[4]),
            "post_type": result[5],
            "likes": result[6],
            "title": result[7],
            "raw_text": result[8]
        }

        data.append(cur_entry)

    page_count = utils.get_total_pages(db.get_full_text_search_count(query)[0])

    data = {
        "search_results": data,
        "page_count": page_count,
        "page": page,
        "query": query,
        "post_url": request.url_root + "categories/",
        "post_type": post_type
    }
    return render_template("search.html", data=data)

@bp.route("/", methods=["POST"])
def search():
    page = request.args.get('page')
    if not page:
        page = 0
    else:
        page = int(page)
    form = request.form
    category = form['search_query']
    category = category.lower()
    search_results = db.search_by_category(category, page=page)

    for search in search_results:
        # print(search[4])
        search[3] = utils.get_elapsed_time(search[3])

    page_count = utils.get_total_pages(db.get_search_count_by_category(category)[0])

    print(db.get_search_count_by_category(category)[0])
    data = {
        "search_results": search_results,
        "page_count": page_count,
        "page": page
    }
    return render_template("search.html", data=data)
from flask import render_template, Blueprint, request
import logging
from utils import PostsHandler
from exceptions import DataLayerError

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')
logging.basicConfig(filename="basic.log", level=logging.INFO)


@main_blueprint.route('/')
def main_page():
    logging.info("запрошена главная страничка")
    return render_template("index.html")


@main_blueprint.route('/search')
def search_page():
    s = request.args.get('s', "")
    posts_handler = PostsHandler("posts.json")
    logging.info("Выполняется поиск")
    try:
        posts = posts_handler.search_posts_for_substring(s)
        return render_template("post_list.html", posts=posts, s=s)
    except DataLayerError:
        return "поврежден файл с данными"

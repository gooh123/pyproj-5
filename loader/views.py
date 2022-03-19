from flask import Blueprint, render_template, request
import logging

from utils import PostsHandler
from exceptions import DataLayerError, PictureWrongTypeError
from loader.utils2 import save_uploader_file


loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='template')
logging.basicConfig(filename="basic.log", level=logging.INFO)


@loader_blueprint.route('/post')
def create_new_post_page():
    return render_template("post_form.html")


@loader_blueprint.route('/post', methods=['POST'])
def create_new_post_from_user_data_page():

    picture = request.files.get("picture", None)
    content = request.form.get("content", None)
    posts_handler = PostsHandler("posts.json")

    if not picture or not content:

        return "данные не загружены"
    try:
        picture_path = save_uploader_file(picture)
    except PictureWrongTypeError:
        logging.info("неверный тип файла")
        return "неверный тип файла"
    except FileNotFoundError:
        logging.info("данные не обнаружены")
        return "не удалось сохранит файл, путь не найден"

    picture_url = "/"+picture_path

    post_object = {"pic": picture_url, "content": content}

    try:
        posts_handler.add_post(post_object)
    except DataLayerError:
        return "не удалось добавить пост, ошибка записи в список постов"

    return render_template("post_uploaded.html", picture_url=picture_url, content=content)

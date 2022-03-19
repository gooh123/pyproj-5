from exceptions import PictureWrongTypeError, PictureUploadError


def save_uploader_file(picture):

    filename = picture.filename

    file_type = filename.split('.')[-1]

    if file_type not in ["jpg", "jpeg", "png", "svg"]:
        raise PictureWrongTypeError

    picture.save(f"./uploads/images/{filename}")

    return f"uploads/images/{filename}"


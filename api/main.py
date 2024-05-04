"""
Image uploader API:
1. Upload image to local file mount/postgres database
2. List all images

Steps:
1. check allowed extensions
2. resize_image
3. upload_image
4. list image
"""

import os
import logging
import cv2
from flask import Flask, request, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# configure logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)

ALLOWED_FILE_EXTENSION = {"jpg", "png", "jpeg"}
TARGET_IMAGE_WIDTH = 1500
app.config["IMAGE_UPLOAD_FOLDER"] = "../uploads"


def check_allowed_file(filename):
    """
    Check allowed image file extension
    :param filename:
    :return:
    """
    return filename.rsplit(".", 1)[1].lower() in ALLOWED_FILE_EXTENSION


def resize_image(image_path, target_width):
    """
    Resize image based on the target_width param maintaining the aspect ratio
    :param image_path: path to the image file to be resized
    :param target_width: desired width of resized image
    :return: None
    """
    img = cv2.imread(image_path)
    if img is None:
        error_msg = f"image not found or could not be opened. {image_path}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
    # check/calculate aspect ratio
    height, width = img.shape[:2]
    aspect_ratio = width / height
    target_height = int(target_width / aspect_ratio)

    # resize the image
    resized_image = cv2.resize(img, (target_width, target_height))
    # save the resized image
    cv2.imwrite(image_path, resized_image)


@app.route("/api/submit", methods=["POST"])
def upload_image():
    """
    Upload image to file store location
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to upload.
    responses:
      201:
        description: Image uploaded successfully.
      400:
        description: Bad request. Invalid image file or no image file found.
      500:
        description: Internal Server Error. Error in resizing image.
    """
    if "file" not in request.files:
        error_msg = "no image file part in request"
        logging.error(error_msg)
        return jsonify({"error": {error_msg}}), 400

    file = request.files["file"]
    if file.filename == "":
        error_msg = "no image file found"
        logging.error(error_msg)
        return jsonify({"error": {error_msg}}), 400

    if file and check_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["IMAGE_UPLOAD_FOLDER"], filename)
        # save the image
        file.save(file_path)
        try:
            # resize image
            resize_image(file_path, TARGET_IMAGE_WIDTH)
            return (
                jsonify({"message": "image uploaded successfully"}),
                201,
            )
        except Exception as e:
            error_msg = f"Error in resizing image: {str(e)}"
            logging.error(error_msg)
            return jsonify({"error": {error_msg}}), 500

    else:
        return jsonify({"error": "invalid image file"}), 400


@app.route("/api/list", methods=["GET"])
def list_images():
    """
    List all images stored in the upload folder along with their urls
    ---
    responses:
      200:
        description: List of image information with image_name and url.
      500:
        description: Internal Server Error. Error listing images.
    """
    image_folder = app.config["IMAGE_UPLOAD_FOLDER"]
    try:
        image_files = os.listdir(image_folder)

        # Create a list of dictionaries containing filename and URL
        images_info = [
            {
                "filename": filename,
                "url": url_for("get_image",
                               image_name=filename, _external=True),
            }
            for filename in image_files
        ]

    except Exception as e:
        error_msg = f"error listing images {str(e)}"
        logging.error(error_msg)
        return jsonify({"error": {error_msg}}), 500

    return jsonify({"images": images_info}), 200


@app.route("/images/<path:image_name>")
def get_image(image_name):
    """
    Retrieve the specified image from the image upload folder
    :param image_name: name of the image file to retrieve
    :return: image file to be sent to the client
    """
    return send_from_directory(app.config["IMAGE_UPLOAD_FOLDER"], image_name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

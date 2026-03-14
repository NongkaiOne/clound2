from flask import Blueprint, request, jsonify
import os

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"

@upload_bp.route("/upload", methods=["POST"])
def upload_file():

    file = request.files["file"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    return jsonify({
        "url": filepath
    })
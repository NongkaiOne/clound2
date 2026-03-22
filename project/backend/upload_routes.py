from flask import Blueprint, request, jsonify
import os

upload_bp = Blueprint("upload", __name__)

# Define the upload folder relative to the instance path or a specific static path
UPLOAD_FOLDER = "uploads" 

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@upload_bp.route("/", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files["file"]

    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    if file:
        # It's safer to use a sanitized filename
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Return a URL that the frontend can use, assuming UPLOAD_FOLDER is served statically
        # This might need adjustment based on how static files are served.
        return jsonify({
            "status": "ok",
            "message": "File uploaded successfully",
            "url": f"/{filepath}" # The URL should be relative to the server's root
        })
    
    return jsonify({"status": "error", "message": "File upload failed"}), 500
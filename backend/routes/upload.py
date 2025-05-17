import os

from flask import Blueprint, jsonify, request
from models.file_metadata import save_metadata
from services.destination_mapper import get_destination, get_similar_destinations
from services.image_classifier import classify_scene
from services.weather_service import get_weather_forecast
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = "./static/uploads"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        scene_type = classify_scene(filepath)
        destination = get_destination(scene_type)
        similar = get_similar_destinations(scene_type, exclude=destination["name"])
        weather = get_weather_forecast(destination["name"])
        save_metadata(filename, scene_type, destination["name"])

        return jsonify(
            {
                "scene_type": scene_type,
                "destination": destination,
                "similar": similar,
                "weather": weather,
                "image_url": f"/static/uploads/{filename}",
            }
        )
    return jsonify({"error": "Invalid file"}), 400

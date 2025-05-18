import os

from flask import Blueprint, jsonify, request
from models.file_metadata import save_metadata
from services.destination_mapper import (
    generate_scene_explanation,
    get_destination,
    get_similar_destinations,
)
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

        scene_type, tags = classify_scene(filepath)
        destination = get_destination(scene_type)
        similar = get_similar_destinations(scene_type, exclude=destination["name"])
        try:
            scene_explanation = generate_scene_explanation(scene_type, tags)
        except Exception as e:
            scene_explanation = "No explanation available"
            print(f"Error generating scene explanation: {e}")

        weather = get_weather_forecast(destination["name"])
        save_metadata(filename, scene_type, destination["name"])

        return jsonify(
            {
                "scene_type": scene_type,
                "scene_explanation": scene_explanation,
                "destination": destination,
                "similar": similar,
                "weather": weather,
                "image_url": f"/static/uploads/{filename}",
            }
        )
    return jsonify({"error": "Invalid file"}), 400

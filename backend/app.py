import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from models.file_metadata import init_db, save_metadata
from services.destination_mapper import get_destination, get_similar_destinations
from services.image_classifier import classify_scene
from services.weather_service import get_weather_forecast
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        scene_type = classify_scene(filepath)
        destination = get_destination(scene_type)
        similar = get_similar_destinations(scene_type)
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


@app.route("/similar", methods=["POST"])
def similar():
    data = request.get_json()
    scene_type = data.get("scene_type")
    if not scene_type:
        return jsonify({"error": "Missing scene_type"}), 400
    return jsonify(get_similar_destinations(scene_type))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

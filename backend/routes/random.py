import random

from flask import Blueprint, jsonify, request
from services.destination_mapper import get_all_destinations
from services.weather_service import get_weather_forecast

random_bp = Blueprint("random", __name__)


@random_bp.route("/random", methods=["GET"])
def random_destination():
    all_destinations = get_all_destinations()
    selected = random.choice(all_destinations)

    weather = get_weather_forecast(selected["name"])

    # Get 3 random others, excluding selected
    similar = random.sample(
        [d for d in all_destinations if d["name"] != selected["name"]], k=3
    )

    return jsonify(
        {
            "scene_type": selected["scene_type"],
            "destination": selected,
            "similar": similar,
            "weather": weather,
            "image_url": selected.get("image"),  # optional field
        }
    )

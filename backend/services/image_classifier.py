import requests
from decouple import config

IMAGGA_AUTH = config("IMAGGA_AUTH")
SCENE_LABELS = [
    "beach",
    "mountain",
    "forest",
    "city",
    "desert",
    "lake",
    "snow",
    "canyon",
    "waterfall",
    "ravine",
    "grassland",
    "volcano",
    "island",
    "coast",
]


def classify_scene(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        headers = {"Authorization": IMAGGA_AUTH}
        response = requests.post(
            "https://api.imagga.com/v2/tags", headers=headers, files=files
        )

    if response.status_code != 200:
        print("Imagga API error:", response.status_code, response.text)
        return "unknown"
    tags = response.json().get("result", {}).get("tags", [])
    if not tags:
        return "unknown"

    for tag in tags:
        label = tag["tag"]["en"].lower()
        confidence = tag["confidence"]
        if confidence >= 35 and label in SCENE_LABELS:
            return label

    return tags[0]["tag"]["en"] if tags else "unknown"


# output = classify_scene("/home/sagar/Downloads/test.jpg")
# print(output)

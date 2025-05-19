# 🚀 Snapshot Trip Planner — Backend

This is the **Flask-based backend** for the Snapshot Trip Planner, powering AI scene detection, destination matching, weather forecasting, and metadata storage.

It is designed to be lightweight, modular, and Docker-ready.

---

## ⚙️ Tech Stack

| Tool/Lib              | Purpose                        |
| --------------------- | ------------------------------ |
| **Flask**             | Core API server                |
| **Python Decouple**   | Config & secrets management    |
| **Requests**          | External API integration       |
| **SQLite**            | Lightweight DB for metadata    |
| **Pillow (optional)** | Image processing               |
| **Docker + Compose**  | Containerization of full stack |

---

## 🌍 Features

-   🔍 **Scene Detection**
    -   Uses Imagga API to tag visual scenes (mountain, beach, city, etc.)
-   🎯 **Destination Matching**
    -   Maps scene to top travel destinations with explanation and metadata
-   🔁 **Similar Destinations**
    -   Ranked list of related spots (activities, season, image, etc.)
-   🌦️ **Weather Forecast**
    -   5-day forecast from OpenWeatherMap
    -   Uses location → fallback to country if location is ambiguous
-   📸 **Image Upload + Metadata**
    -   Upload endpoint stores file and logs metadata to DB

---

## 📁 Project Structure

```
├── app.py                  # Entry point for Flask app
├── config.py               # Loads env/config variables
├── requirements.txt        # Python dependencies
├── models/
│ └── file_metadata.py      # SQLite model to store uploads
├── services/
│ ├── image_classifier.py   # Handles Imagga integration
│ ├── destination_mapper.py # Maps scene type to destinations
│ └── weather_service.py    # Handles weather + fallback logic
├── utils/
│ └── cache.py              # (Optional) Caching support
└── static/uploads/         # Stores uploaded image files
```

## 🔌 Environment Variables

Use Python Decouple via `.env` (or Docker secrets):

```env
IMAGGA_API_KEY=your_key
IMAGGA_API_SECRET=your_secret

OPENWEATHER_API_KEY=your_openweathermap_key

# Optional:
FLASK_ENV=development
```

## 📦 API Routes

### `POST /upload`

-   Accepts image file
-   Returns:

    -   `scene_type`

    -   `destination`

    -   `similar`

    -   `weather[]`

    -   `image_url`

### `GET /random`

-   Picks a random destination

-   Returns same structure as /upload

-   "Similar" results are scene-agnostic random picks

### `GET /ping`

-   Health check → returns `{ "status": "ok" }`

### 📸 Scene Detection

-   Uses Imagga /v2/tags endpoint with uploaded image

-   Filters high-confidence tags (e.g. > 90%)

-   Maps to internal scene types:

    -   `mountain`, `beach`, `city`, `forest`, `desert`, `island`, etc.

### 🗺️ Destination Mapping

Each scene type is mapped to 5+ curated destinations:

```python
{
  "scene_type": "island",
  "name": "Bora Bora",
  "activities": ["Snorkeling", "Scuba Diving", "Sunbathing"],
  "image": "https://cdn.pixabay.com/photo/...",
  "country": "French Polynesia",
  "bestSeason": "May–October"
}
```

Destinations include:

-   Rank
-   Activities
-   Country (used as weather fallback)
-   Best season
-   Image URL (Pixabay, Pexels, or static)

### 🌤️ Weather Service

-   Uses OpenWeatherMap Geocoding → 7-day Forecast
-   If specific destination is not found, it tries the country as fallback
-   If still not found → returns []

Returns up to 5 daily summaries with:

-   `date`, `temp`, `humidity`, `icon`, `description`

### 💾 Metadata Storage

-   Uses SQLite to store upload records:
    -   Filename
    -   Scene type
    -   Timestamp
-   Future-proof: can be extended to track user uploads, trip history, etc.

### 🐳 Dockerized Setup

The backend is Docker-ready and included in root docker-compose.yml:

```bash
docker-compose up --build
```

Runs on port 5000 inside container.

### ✅ Example Response

```json
{
  "scene_type": "island",
  "destination": {
    "name": "Bora Bora",
    "rank": 1,
    "activities": ["Snorkeling", "Scuba Diving"],
    "image": "https://cdn.pixabay.com/...",
    "country": "French Polynesia",
    "bestSeason": "May to October"
  },
  "similar": [
    { "name": "Maldives", "rank": 2, ... },
    { "name": "Phuket", "rank": 3, ... }
  ],
  "weather": [
    {
      "date": "2025-05-20",
      "temp": 29.3,
      "humidity": 78,
      "description": "clear sky",
      "icon": "01d"
    }
  ],
  "image_url": "/static/uploads/7.jpg"
}
```

### 🧪 Testing Tips

-   Upload images of beaches, forests, etc. and check match
-   Use /random to test random flow (bypasses image upload)
-   Test destinations that don't resolve directly (e.g., Bora Bora) to verify fallback to country
-   Monitor logs for fallback messages and geolocation behavior

### 🧱 Future Enhancements

-   Redis caching of geolocation & weather results.
-   Use S3 or other storages for persistent files like image uploads.

-   Use LLM to auto-generate destination descriptions.

-   Support user accounts and trip planning.

-   Replace Imagga with custom local scene model (e.g., CLIP/BLIP).

-   Support reverse search: "Show me destinations like Iceland".

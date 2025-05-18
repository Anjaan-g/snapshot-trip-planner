# Snapshot Trip Planner

AI-powered travel inspiration based on your uploaded photos. Built with:

-   🌐 **Frontend**: Next.js 15 (App Router, TypeScript, Tailwind CSS, shadcn/ui)
-   🔙 **Backend**: Flask with Imagga scene recognition + OpenWeather API
-   🐳 **Deployment**: Vercel (frontend) + Render (backend)

---

## 🧠 What It Does

1. Upload a scenic photo (e.g., mountains, beaches, cities)
2. AI detects the dominant **scene type**
3. Suggests a travel destination based on the scene
4. Shows a 7-day weather forecast for that destination (cached for 1 hour)
5. Lets you explore 3 similar destinations ranked by relevance

---

## 🖼️ Frontend (`/frontend`)

### Tech Stack

-   [Next.js 15+](https://nextjs.org/) (App Router)
-   TypeScript
-   Tailwind CSS + [shadcn/ui](https://ui.shadcn.com/)
-   Fetch API for backend integration
-   Absolute imports with `@/` alias
-   Dynamic background image from local folder
-   File upload with live preview
-   "Suggest Random" button for exploration

### Local Dev

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

---

## ⚙️ Backend (`/backend`)

### Tech Stack

-   Flask (with CORS)
-   Imagga API for image tagging (scene detection)
-   OpenWeatherMap API for 7-day forecast
-   SQLite for storing file + scene metadata
-   Dockerized for easy deployment

### API Endpoints

-   `POST /upload` — Uploads an image and returns scene, destination, weather
-   `POST /similar` — Returns 3 similar destinations based on scene type, sorted by rank
-   `GET /ping` — Warm-up endpoint for Render cold starts
-   `GET /random` — Returns a random destination

### Local Dev

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Environment Variables

Create `.env`:

```
OPENWEATHER_API_KEY=...
IMAGGA_AUTH=Basic <your-auth-header>
```

### Persistent Files

-   Uploaded images → `/static/uploads/`
-   Metadata stored in `metadata.db` (SQLite)

---

## 🐳 Docker Compose (optional for self-hosted)

```bash
docker-compose up --build
```

(Port 80 may need to be changed if in use. Recommend using port 8080.)

---

## 🚀 Deployment

-   **Frontend** → [Vercel](https://vercel.com/)

    -   Auto deploys from GitHub
    -   Set `NEXT_PUBLIC_BACKEND_URL` to Render URL

-   **Backend** → [Render.com](https://render.com/)

    -   Use Docker or Gunicorn deployment
    -   Add persistent disk volume
    -   Add `/ping` route to warm up

---

## 🧪 Ping Route (to prevent cold starts)

Added in Flask backend:

```python
@app.route('/ping')
def ping():
    return jsonify({"message": "pong"}), 200
```

---

## 📝 Notes

> ⚠️ First load of backend (Render free tier) may take \~5–10 seconds due to cold start.

> Uploaded images and DB are stored in a Render persistent volume.

> Imagga API is used to avoid large ML dependencies like PyTorch.

> Destination logic randomly picks one ranked location per scene and returns 3 similar ones sorted by rank.

---

### 🧱 Scaling Considerations

-   Swap in flask-caching + Redis for multi-worker caching

-   Use PostgreSQL + auth for user trip history

-   Switch to persistent object storage (S3, Cloudinary) for image uploads

-   Migrate to One Call API for accurate 7-day weather

-   Replace Imagga with a local ML model for custom scene detection

### 🧑‍💻 Author

Built by Sagar — Senior Full Stack Developer

---

### License

MIT

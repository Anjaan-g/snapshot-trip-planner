# 📸 Snapshot Trip Planner — Frontend

This is the **Next.js 14 App Router** frontend for the Snapshot Trip Planner — a visually dynamic, AI-powered travel discovery tool.

The app lets users:

- Upload scenic photos to detect landscapes via AI
- Suggest matching travel destinations
- Show weather forecasts
- Explore similar destinations
- Get random suggestions

---

## 🔧 Tech Stack

| Tool/Lib          | Purpose                                |
| ----------------- | -------------------------------------- |
| **Next.js 15+**   | App Router structure + SSR/ISR         |
| **TypeScript**    | Strong typing across the app           |
| **Tailwind CSS**  | Utility-first styling                  |
| **shadcn/ui**     | Accessible, customizable UI components |
| **Framer Motion** | Transitions and animations             |
| **ApexCharts**    | Beautiful charts for weather data      |

---

## 📁 Folder Structure

```
src/
├── app/ # Next.js app router structure
│ ├── layout.tsx # Base layout, includes background and theme
│ └── page.tsx # Home page logic + state
├── components/
│ ├── ui/ # All shadcn/ui components
│ ├── planner/ # App-specific UI: DestinationInfo, UploadForm, etc.
│ └── weather/ # WeatherForecast.tsx with ApexCharts
├── types/
│ └── planner.ts # Type definitions for backend responses
├── utils/
│ └── api.ts # All backend API fetchers (upload, random, etc.)
├── public/
│ └── images/ # Local background or fallback images
└── styles/
└── globals.css # Tailwind + base styles
```

## 📌 Key Features

### 🖼 Upload & Analyze

- Upload `.jpg/.png` images (max 10MB)
- Drag & drop or browse
- Auto previews image
- Validates file type and size
- Clears input easily

### 🧠 AI Scene Detection

- Uses Imagga to extract scene tags
- Maps to relevant destination via backend
- Shows match with explanation, image, and metadata

### 🌍 Similar Destinations

- Ranked suggestions based on scene type
- Shows rank, image, activities, and best season
- "Show me more like this" toggles similar view

### 🌦️ 5-Day Weather Forecast

- Uses OpenWeatherMap for real data
- Bar chart with dynamic coloring
- Emoji + icon + temperature + humidity per day
- Supports °C/°F toggle

### 🎲 Random Destination

- One-click surprise
- Chooses a random scenic destination across the world
- Skips scene detection and jumps straight to recommendations

---

## 💡 Design Decisions

- Used `App Router` for Next.js to align with modern architecture
- All backend calls routed through `/utils/api.ts` (single responsibility)
- Weather chart prefers real data, fallback to country if location fails
- UI emphasizes clean, modern, vibrant feel inspired by Google Travel
- All styling is managed with Tailwind CSS and shadcn/ui primitives
- Animations use Framer Motion for subtle polish

---

## 🚫 Input Constraints

- File size max: **10MB**
- File types: `image/jpg`, `image/jpeg`, `image/png`
- No upload = disabled buttons
- No weather = fallback UI block (graceful)

---

## 🚀 How to Run Frontend

### Using Docker
```bash
# From root project directory:
docker-compose up --build
```

### Or locally:

```
cd frontend
npm install
npm run dev
```

## 📝 TODOs or Future Enhancements

Mobile responsiveness polish

Add loading spinner during image analysis

Paginate similar destinations

Add auth & save plans to user account

Real-time country search or destination search

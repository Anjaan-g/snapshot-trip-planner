export interface Destination {
  name: string;
  rank: number;
  explanation: string;
  activities: string[];
  bestSeason: string;
  country: string;
  image: string;
}

export interface WeatherDay {
  date: string; // ISO string
  description: string; // "Clear", "Rain", etc.
  temp: number; // Celsius
  humidity: number; // 0–100
}

export interface UploadResult {
  scene_type: string;
  destination: Destination;
  weather: WeatherDay[];
  similar: Destination[];
  image_url?: string;
  scene_explanation?: string;
}

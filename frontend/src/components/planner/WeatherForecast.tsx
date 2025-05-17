"use client";

import dynamic from "next/dynamic";
import { format, parseISO } from "date-fns";
import { WeatherDay } from "@/types/planner";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

import { CloudRain, Sun, Cloud, Zap, Snowflake } from "lucide-react";

const ApexChart = dynamic(() => import("react-apexcharts"), { ssr: false });

interface Props {
  forecast: WeatherDay[];
  unit?: "metric" | "imperial";
}

function getBarColor(temp: number): string {
  if (temp < 5) return "#3b82f6"; // Blue
  if (temp < 15) return "#60a5fa"; // Light Blue
  if (temp < 25) return "#facc15"; // Yellow
  return "#f87171"; // Red
}

function getIcon(description: string) {
  const desc = description.toLowerCase();
  if (desc.includes("thunder"))
    return <Zap className="w-5 h-5 text-yellow-400" />;
  if (desc.includes("rain"))
    return <CloudRain className="w-5 h-5 text-blue-500" />;
  if (desc.includes("snow"))
    return <Snowflake className="w-5 h-5 text-cyan-300" />;
  if (desc.includes("cloud"))
    return <Cloud className="w-5 h-5 text-gray-600" />;
  return <Sun className="w-5 h-5 text-yellow-400" />;
}

function getEmoji(description: string): string {
  const desc = description.toLowerCase();
  if (desc.includes("thunder")) return "⚡";
  if (desc.includes("rain")) return "🌧️";
  if (desc.includes("snow")) return "❄️";
  if (desc.includes("cloud")) return "☁️";
  return "☀️";
}

export default function WeatherForecast({ forecast, unit = "metric" }: Props) {
  const categories = forecast.map((day) => format(parseISO(day.date), "EEE"));
  const temps = forecast.map((day) => day.temp);

  const barColors = temps.map(getBarColor);

  const options: ApexCharts.ApexOptions = {
    chart: {
      type: "bar",
      toolbar: { show: false },
      foreColor: "#111",
    },
    plotOptions: {
      bar: {
        distributed: true,
        borderRadius: 6,
        columnWidth: "40%",
      },
    },
    xaxis: {
      categories,
      labels: {
        style: {
          colors: "#444",
          fontWeight: 600,
        },
      },
    },
    yaxis: {
      title: {
        text: unit === "metric" ? "°C" : "°F",
        style: { color: "#444" },
      },
      labels: {
        formatter: (val) => `${val}°`,
        style: { colors: "#666" },
      },
    },
    colors: barColors,
    tooltip: {
      shared: true,
      intersect: false,
      y: {
        formatter: (val: number) => `${val}°${unit === "metric" ? "C" : "F"}`,
      },
    },
    grid: {
      borderColor: "#e5e7eb",
    },
    dataLabels: {
      enabled: true,
      style: { colors: ["#111"] },
      formatter: (val) => Math.round(Number(val)),
    },
  };

  const series = [
    {
      name: "Temperature",
      data: temps,
    },
  ];

  if (!forecast || forecast.length === 0) {
    return (
      <Card className="text-center bg-white/10 border border-white/10 text-white">
        <CardHeader>
          <CardTitle>7-Day Weather Forecast</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-300">
            Weather data is currently unavailable.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-white max-w-4xl mx-auto border border-gray-200 text-gray-900 shadow-xl">
      <CardHeader>
        <CardTitle>7-Day Weather Forecast</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="w-full h-64">
          <ApexChart
            options={options}
            series={series}
            type="bar"
            height="100%"
            width="100%"
          />
        </div>

        {/* Icon/Label Grid */}
        <div
          className="grid gap-2 mt-4 text-center max-w-3xl mx-8"
          style={{
            gridTemplateColumns: `repeat(${forecast.length}, minmax(0, 1fr))`,
          }}
        >
          {forecast.map((day, index) => {
            const emoji = getEmoji(day.description);
            const desc = day.description.toLowerCase();
            const colorClass = desc.includes("sun")
              ? "text-yellow-500"
              : desc.includes("rain")
              ? "text-blue-500"
              : desc.includes("cloud")
              ? "text-gray-500"
              : desc.includes("snow")
              ? "text-cyan-400"
              : "text-pink-500";

            return (
              <div
                key={index}
                className="flex flex-col items-center text-xs min-w-0 "
              >
                <div className="text-2xl">{emoji}</div>
                {/* {getIcon(day.description)} */}
                <p className="font-medium">
                  {format(parseISO(day.date), "EEE")}
                </p>
                <p className={`capitalize font-semibold ${colorClass}`}>
                  {day.description}
                </p>
                <p className="text-black font-semibold">
                  {Math.round(day.temp)}°{unit === "metric" ? "C" : "F"}
                </p>
                <p className="text-blue-600 text-xs">
                  {day.humidity}% humidity
                </p>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

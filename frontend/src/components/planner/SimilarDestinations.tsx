"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Destination } from "@/types/planner";
import { useEffect, useRef } from "react";

interface Props {
  destinations: Destination[];
  scene: string;
  autoScroll?: boolean;
}

export default function SimilarDestinations({
  destinations,
  scene,
  autoScroll,
}: Props) {
  const ref = useRef<HTMLDivElement | null>(null);
  const sorted = [...destinations].sort((a, b) => a.rank - b.rank);

  useEffect(() => {
    if (autoScroll && ref.current) {
      ref.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [autoScroll]);

  if (!destinations || destinations.length === 0) {
    return (
      <div className="mt-8 text-center text-sm text-gray-400">
        No similar destinations found.
      </div>
    );
  }

  return (
    <div
      ref={ref}
      className="mt-10 space-y-4 max-w-4xl mx-auto animate-fade-in transition-opacity duration-500"
    >
      <h2
        className="text-2xl font-bold text-white px-4 py-2 rounded-md relative inline-block z-10
               bg-gradient-to-r from-pink-600 via-red-500 to-yellow-400 bg-opacity-80 shadow-md"
      >
        Similar Destinations
      </h2>

      <div className="flex flex-col space-y-4">
        {sorted
          .filter((d) => d?.name && d?.explanation)
          .map((dest, i) => (
            <Card
              key={dest.name}
              className="relative overflow-hidden border border-white/10"
            >
              <CardHeader>
                <CardTitle className="text-lg font-bold">
                  #{i + 1} · {dest.name}
                </CardTitle>
                <div className="text-sm text-muted-foreground">
                  {dest.explanation}
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col space-y-2">
                  {/* <p>
									<strong>Scene Type:</strong> {scene.toUpperCase()}
								</p> */}
                  <p>
                    <strong>Country:</strong> {dest.country}
                  </p>
                  <p>
                    <strong>Best time to visit:</strong> {dest.bestSeason}
                  </p>
                  <p>
                    <strong>Activities:</strong> {dest.activities.join(", ")}
                  </p>
                  <div>
                    <strong>Description:</strong>{" "}
                    <p className="text-muted-foreground">{dest.explanation}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
      </div>
    </div>
  );
}

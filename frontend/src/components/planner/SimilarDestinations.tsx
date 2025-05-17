"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Destination } from "@/types/planner";

interface Props {
  destinations: Destination[];
  scene: string;
}

export default function SimilarDestinations({ destinations, scene }: Props) {
  const sorted = [...destinations].sort((a, b) => a.rank - b.rank);
  if (!destinations || destinations.length === 0) {
    return (
      <div className="mt-8 text-center text-sm text-gray-400">
        No similar destinations found.
      </div>
    );
  }

  return (
    <div className="mt-10 space-y-4 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold bg-gradient-to-r from-pink-500 via-red-500 to-yellow-400 bg-clip-text text-transparent">
        Similar Destinations for <span className="capitalize">{scene}</span>{" "}
        scenes
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

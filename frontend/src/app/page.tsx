"use client";

import { useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import { UploadResult } from "@/types/planner";
import DestinationInfo from "@/components/planner/DestinationInfo";
import WeatherForecast from "@/components/planner/WeatherForecast";
import SimilarDestinations from "@/components/planner/SimilarDestinations";
import SkeletonLoader from "@/components/loader";
import { getRandomDestination, uploadImage } from "@/utils/api";
import UploadForm from "@/components/planner/UploadForm";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<UploadResult | null>(null);
  const [unit, setUnit] = useState<"metric" | "imperial">("metric");
  const [showSimilar, setShowSimilar] = useState(false);
  const similarRef = useRef<HTMLDivElement | null>(null);

  const handleUnitToggle = () => {
    setUnit((prev) => (prev === "metric" ? "imperial" : "metric"));
  };
  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setResult(null);

    try {
      const data = await uploadImage(file);
      setResult(data);
    } catch (err) {
      console.error(err);
      // optionally show error UI here
    } finally {
      setUploading(false);
    }
  };

  const handleRandom = async () => {
    setUploading(true);
    setFile(null);
    setShowSimilar(false);
    setResult(null);

    try {
      const data = await getRandomDestination();
      setResult(data);
    } catch (err) {
      console.error(err);
      // optionally show error UI here
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="w-full my-4">
      <UploadForm
        file={file}
        setFile={setFile}
        uploading={uploading}
        onFileSelect={setFile}
        onUpload={handleUpload}
        onRandom={handleRandom}
        result={result}
        setResult={setResult}
      />

      {/* Result or Loading */}
      <AnimatePresence mode="wait">
        {uploading && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="mt-8"
          >
            <SkeletonLoader />
          </motion.div>
        )}

        {!uploading && result && (
          <motion.div
            key="result"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-8 space-y-6 text-left w-full"
          >
            <DestinationInfo
              data={result.destination}
              onShowMore={
                result.similar?.length > 0
                  ? () => {
                      setShowSimilar(true);
                    }
                  : undefined
              }
            />
            {result.weather?.length > 0 ? (
              <WeatherForecast forecast={result.weather} />
            ) : (
              <>
                <Card className="max-w-4xl mx-auto p-8 bg-white backdrop-blur-lg border border-white/20 rounded-2xl shadow-lg mt-5">
                  <CardHeader className="text-center">
                    <h2 className="text-2xl font-bold">Weather Forecast</h2>
                  </CardHeader>
                  <CardContent>
                    <p className="text-lg text-gray-500">
                      No weather data available for this destination.
                    </p>
                  </CardContent>
                </Card>
              </>
            )}

            {showSimilar && result?.similar?.length > 0 && (
              <div ref={similarRef}>
                <SimilarDestinations
                  destinations={result.similar}
                  scene={result.scene_type}
                  autoScroll
                />
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

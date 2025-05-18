"use client";

import React, { useRef, useState, DragEvent } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { UploadCloud, Sparkles, CrossIcon, X } from "lucide-react";
import { UploadResult } from "@/types/planner";

interface Props {
  onFileSelect: (file: File) => void;
  onUpload: () => void;
  onRandom: () => void; // Added prop for random button click
  uploading: boolean;
  file: File | null;
  setFile: (file: File | null) => void;
  result?: UploadResult | null;
  setResult?: (result: UploadResult | null) => void;
}

export default function UploadForm({
  onFileSelect,
  onUpload,
  onRandom,
  uploading,
  file,
  setFile,
  result,
  setResult,
}: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const MAX_FILE_SIZE_MB = 10 * 1024 * 1024;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (!file) return;

    if (file) {
      if (file.size > MAX_FILE_SIZE_MB) {
        alert("File size exceeds 10MB");
        return;
      }
      onFileSelect(file);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) {
      onFileSelect(dropped);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result as string);
      reader.readAsDataURL(dropped);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
  };

  const clearFile = () => {
    setFile(null);
    setPreview(null);
    setResult?.(null);
  };

  const handleClear = () => {
    if (inputRef.current) {
      inputRef.current.value = ""; // clears native input
    }
    clearFile();
  };

  return (
    <Card className="max-w-4xl mx-auto p-8 bg-white backdrop-blur-lg border border-white/20 rounded-2xl shadow-lg mt-5">
      <CardHeader className="text-center">
        <CardTitle className="text-4xl font-extrabold bg-gradient-to-r from-pink-500 via-red-500 to-yellow-400 bg-clip-text text-transparent mb-2">
          AI Trip Planner
        </CardTitle>
        <p className="text-gray-600">
          Upload a scenic photo or let AI surprise you ✨
        </p>
      </CardHeader>

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => inputRef.current?.click()}
        className={`relative cursor-pointer border-2 border-dashed rounded-lg p-6 max-w-4xl flex flex-col items-center justify-center text-gray-400 transition
          			${
                  dragOver
                    ? "border-pink-500 bg-pink-50/20 text-pink-400"
                    : "border-gray-400 bg-transparent"
                }`}
      >
        {!file ? (
          <>
            <Input
              ref={inputRef}
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="absolute inset-0 opacity-0 cursor-pointer"
              aria-label="File upload"
            />
            <span>Drag & drop an image here, or click to select</span>
          </>
        ) : (
          <>
            <div className="mt-6 h-[200px] flex items-center justify-center relative border border-white/10 rounded-xl overflow-hidden bg-white/5 w-full max-w-md">
              <img
                src={preview ?? undefined}
                alt="Preview"
                className="object-contain rounded-lg"
                style={{ maxHeight: "200px", maxWidth: "100%" }}
              />
            </div>
            {result && (
              <>
                <p className="mx-auto mt-2 text-gray-700 dark:text-gray-300">
                  <strong>Detected Scene: </strong>{" "}
                  {result.scene_type.toUpperCase()}
                </p>
                <p className="mx-auto mt-2 text-gray-700 dark:text-gray-300">
                  <strong>Explanation: </strong> {result.scene_explanation}
                </p>
              </>
            )}
          </>
        )}
      </div>

      <div className="mt-6 flex justify-center gap-4">
        {!result && (
          <Button
            onClick={onUpload}
            disabled={uploading || !file || !!result}
            className="flex items-center gap-2"
          >
            <UploadCloud />
            {uploading ? "Uploading..." : "Analyze Image"}
          </Button>
        )}

        <Button
          variant="outline"
          onClick={onRandom}
          disabled={uploading}
          className="flex items-center gap-2"
        >
          <Sparkles />
          Suggest Random
        </Button>

        {file && (
          <Button
            variant="outline"
            onClick={handleClear}
            className="text-sm text-red-500 hover:text-red-700"
          >
            ❌ Try With Another Image
          </Button>
        )}
      </div>
    </Card>
  );
}

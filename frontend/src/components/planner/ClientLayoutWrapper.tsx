"use client";
import { ReactNode, useEffect, useState } from "react";

import React from "react";
const fallback = [
  "/bg/1.jpg",
  "/bg/2.jpg",
  "/bg/3.jpg",
  "/bg/4.jpg",
  "/bg/5.jpg",
  "/bg/6.jpg",
  "/bg/7.jpg",
  "/bg/8.jpg",
  "/bg/9.jpg",
  "/bg/10.jpg",
  "/bg/11.jpg",
  "/bg/12.jpg",
  "/bg/13.jpg",
  "/bg/14.jpg",
  "/bg/15.jpg",
  "/bg/16.jpg",
  "/bg/17.jpg",
  "/bg/18.jpg",
  "/bg/19.jpg",
  "/bg/20.jpg",
];

const ClientLayoutWrapper = ({ children }: { children: ReactNode }) => {
  const [bgImage, setBgImage] = useState<string>(fallback[0]);

  useEffect(() => {
    const randomLocal = fallback[Math.floor(Math.random() * fallback.length)];
    setBgImage(randomLocal);
  }, []);

  return (
    <div
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "fixed",
      }}
      className="min-h-screen text-white font-sans antialiased relative w-full"
    >
      <div className="absolute inset-0 bg-black/50 -z-10" />
      <main className="relative flex flex-col items-center justify-center min-h-screen px-4 w-full">
        {children}
      </main>
    </div>
  );
};

export default ClientLayoutWrapper;

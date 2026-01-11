"use client"

import React, { useEffect, useState } from "react";
import Lottie from "lottie-react";

type LottieHeroProps = {
  speed?: number; // playback speed multiplier (1 = normal)
  loop?: boolean;
  width?: string;
  height?: string;
};

export default function LottieHero({ speed = 1, loop = true, width = "100%", height = "12rem" }: LottieHeroProps) {
  const [animationData, setAnimationData] = useState<any | null>(null);
  const lottieRef = React.useRef<any>(null);

  useEffect(() => {
    let mounted = true;
    // Load local Lottie JSON from `public/animations/hero.json` for offline/dev reliability.
    fetch("/animations/hero.json")
      .then((r) => r.json())
      .then((j) => {
        if (mounted) setAnimationData(j);
      })
      .catch(() => {
        /* ignore */
      });
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (lottieRef.current && typeof lottieRef.current.setSpeed === "function") {
      try {
        lottieRef.current.setSpeed(speed);
      } catch {}
    }
  }, [speed, animationData]);

  return (
    <div className="w-full flex justify-center mb-4">
      {animationData ? (
        <div style={{ width, height, maxWidth: "48rem" }} className="rounded-lg overflow-hidden">
          <Lottie lottieRef={lottieRef} animationData={animationData} loop={loop} autoplay />
        </div>
      ) : (
        <div style={{ width, height }} className="rounded-lg bg-white/5" />
      )}
    </div>
  );
}

"use client"

import React from "react";

export default function AnimatedHero() {
  return (
    <div className="w-full flex justify-center mb-4">
      <svg className="w-full max-w-3xl h-48 rounded-lg shadow-sm" viewBox="0 0 1200 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="g1">
            <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.9">
              <animate attributeName="stop-color" dur="6s" values="#06b6d4;#00a3ff;#3ddc97;#06b6d4" repeatCount="indefinite" />
            </stop>
            <stop offset="100%" stopColor="#3ddc97" stopOpacity="0.8">
              <animate attributeName="stop-color" dur="6s" values="#3ddc97;#06b6d4;#00a3ff;#3ddc97" repeatCount="indefinite" />
            </stop>
          </linearGradient>
        </defs>

        <rect x="0" y="0" width="1200" height="200" rx="16" fill="url(#g1)" opacity="0.12" />

        <g transform="translate(40,24)">
          <rect x="0" y="20" width="420" height="120" rx="12" fill="#0f172a" opacity="0.06" />
          <g transform="translate(16,12)">
            <rect width="160" height="14" rx="7" fill="#fff" opacity="0.12" />
            <rect y="28" width="300" height="10" rx="6" fill="#fff" opacity="0.08" />
          </g>
        </g>

        <g transform="translate(520,24)">
          <circle cx="120" cy="80" r="56" fill="#fff" opacity="0.04" />
          <text x="40" y="95" fill="#94a3b8" fontFamily="Cairo, Arial, sans-serif" fontSize="18">تقييم فوري</text>
        </g>
      </svg>
    </div>
  );
}

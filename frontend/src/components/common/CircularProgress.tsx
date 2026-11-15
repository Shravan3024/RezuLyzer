import React from 'react';

interface CircularProgressProps {
  score: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
  category?: string;
}

export const CircularProgress: React.FC<CircularProgressProps> = ({
  score,
  size = 180,
  strokeWidth = 14,
  label = 'ATS Score',
  category,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const clampedScore = Math.min(100, Math.max(0, score));
  const strokeDashoffset = circumference - (clampedScore / 100) * circumference;

  // Determine color scheme
  let strokeColor = '#3b82f6'; // blue
  let textColor = 'text-blue-600';
  let badgeBg = 'bg-blue-50 text-blue-700 border-blue-200';

  if (clampedScore >= 85) {
    strokeColor = '#10b981'; // emerald
    textColor = 'text-emerald-600';
    badgeBg = 'bg-emerald-50 text-emerald-700 border-emerald-200';
  } else if (clampedScore >= 70) {
    strokeColor = '#2563eb'; // blue
    textColor = 'text-blue-600';
    badgeBg = 'bg-blue-50 text-blue-700 border-blue-200';
  } else if (clampedScore >= 50) {
    strokeColor = '#f59e0b'; // amber
    textColor = 'text-amber-600';
    badgeBg = 'bg-amber-50 text-amber-700 border-amber-200';
  } else {
    strokeColor = '#f43f5e'; // rose
    textColor = 'text-rose-600';
    badgeBg = 'bg-rose-50 text-rose-700 border-rose-200';
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#e2e8f0"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Foreground animated score circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center label & number */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className={`text-4xl font-extrabold tracking-tight ${textColor}`}>
            {clampedScore.toFixed(0)}
          </span>
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            out of 100
          </span>
        </div>
      </div>

      {/* Category Pill */}
      {category && (
        <div className={`mt-3 px-3 py-1 rounded-full text-xs font-semibold border ${badgeBg}`}>
          {category}
        </div>
      )}
      <span className="text-xs text-slate-500 font-medium mt-1">{label}</span>
    </div>
  );
};


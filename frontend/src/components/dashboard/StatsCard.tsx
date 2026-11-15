import React, { ReactNode } from 'react';

interface StatsCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: ReactNode;
  trend?: string;
  colorScheme?: 'blue' | 'emerald' | 'amber' | 'indigo' | 'purple';
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  trend,
  colorScheme = 'blue',
}) => {
  const colorMap = {
    blue: {
      bg: 'bg-blue-50 text-blue-700 border-blue-100',
      iconBg: 'bg-blue-600 text-white',
    },
    emerald: {
      bg: 'bg-emerald-50 text-emerald-700 border-emerald-100',
      iconBg: 'bg-emerald-600 text-white',
    },
    amber: {
      bg: 'bg-amber-50 text-amber-700 border-amber-100',
      iconBg: 'bg-amber-600 text-white',
    },
    indigo: {
      bg: 'bg-indigo-50 text-indigo-700 border-indigo-100',
      iconBg: 'bg-indigo-600 text-white',
    },
    purple: {
      bg: 'bg-purple-50 text-purple-700 border-purple-100',
      iconBg: 'bg-purple-600 text-white',
    },
  };

  const scheme = colorMap[colorScheme];

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-500">{title}</span>
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center shadow-xs ${scheme.iconBg}`}>
          {icon}
        </div>
      </div>

      <div className="mt-4 flex items-baseline justify-between">
        <span className="text-3xl font-extrabold text-slate-900 tracking-tight">{value}</span>
        {trend && (
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${scheme.bg}`}>
            {trend}
          </span>
        )}
      </div>

      {subtitle && <p className="mt-1 text-xs text-slate-500">{subtitle}</p>}
    </div>
  );
};


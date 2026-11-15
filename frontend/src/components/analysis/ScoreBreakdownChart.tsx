import React from 'react';
import { ScoreBreakdown } from '../../types';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

interface ScoreBreakdownChartProps {
  breakdown: ScoreBreakdown;
}

export const ScoreBreakdownChart: React.FC<ScoreBreakdownChartProps> = ({ breakdown }) => {
  const chartData = [
    {
      name: 'Required Skills',
      score: breakdown.required_skills?.score || 0,
      weight: breakdown.required_skills?.weight || 35,
      contribution: breakdown.required_skills?.weighted_contribution || 0,
      color: '#2563eb',
    },
    {
      name: 'Semantic Sim.',
      score: breakdown.semantic_similarity?.score || 0,
      weight: breakdown.semantic_similarity?.weight || 25,
      contribution: breakdown.semantic_similarity?.weighted_contribution || 0,
      color: '#4f46e5',
    },
    {
      name: 'Keywords',
      score: breakdown.keyword_relevance?.score || 0,
      weight: breakdown.keyword_relevance?.weight || 15,
      contribution: breakdown.keyword_relevance?.weighted_contribution || 0,
      color: '#0891b2',
    },
    {
      name: 'Experience',
      score: breakdown.experience_relevance?.score || 0,
      weight: breakdown.experience_relevance?.weight || 10,
      contribution: breakdown.experience_relevance?.weighted_contribution || 0,
      color: '#059669',
    },
    {
      name: 'Education',
      score: breakdown.education_relevance?.score || 0,
      weight: breakdown.education_relevance?.weight || 10,
      contribution: breakdown.education_relevance?.weighted_contribution || 0,
      color: '#d97706',
    },
    {
      name: 'Structure',
      score: breakdown.resume_structure?.score || 0,
      weight: breakdown.resume_structure?.weight || 5,
      contribution: breakdown.resume_structure?.weighted_contribution || 0,
      color: '#7c3aed',
    },
  ];

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900">Score Breakdown & Weights</h3>
          <p className="text-xs text-slate-500">
            Multi-factor evaluation normalized from 0 to 100 with weighted contribution
          </p>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
            <XAxis
              dataKey="name"
              tick={{ fontSize: 11, fill: '#64748b' }}
              interval={0}
              angle={-20}
              textAnchor="end"
            />
            <YAxis
              domain={[0, 100]}
              tick={{ fontSize: 11, fill: '#64748b' }}
              ticks={[0, 25, 50, 75, 100]}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload;
                  return (
                    <div className="bg-slate-900 text-white p-3 rounded-xl shadow-lg text-xs space-y-1">
                      <p className="font-bold text-sm text-slate-100">{data.name}</p>
                      <p className="text-slate-300">
                        Score: <span className="font-semibold text-white">{data.score.toFixed(1)} / 100</span>
                      </p>
                      <p className="text-slate-300">
                        Weight: <span className="font-semibold text-white">{data.weight}%</span>
                      </p>
                      <p className="text-emerald-400 font-semibold pt-1 border-t border-slate-700">
                        ATS Points: +{data.contribution.toFixed(1)} pts
                      </p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Bar dataKey="score" radius={[6, 6, 0, 0]} maxBarSize={45}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Numerical breakdown table */}
      <div className="mt-4 pt-4 border-t border-slate-100 grid grid-cols-2 sm:grid-cols-3 gap-3">
        {chartData.map((item) => (
          <div key={item.name} className="p-2.5 rounded-xl bg-slate-50 border border-slate-100">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-600 truncate">{item.name}</span>
              <span className="text-[10px] font-semibold text-slate-400">{item.weight}%</span>
            </div>
            <div className="mt-1 flex items-baseline justify-between">
              <span className="text-sm font-bold text-slate-800">{item.score.toFixed(1)}%</span>
              <span className="text-xs text-blue-600 font-semibold">+{item.contribution.toFixed(1)} pts</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};


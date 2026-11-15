import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  FileText,
  BarChart3,
  Award,
  Clock,
  ArrowRight,
  Upload,
  Briefcase,
  GitCompare,
  TrendingUp,
  AlertCircle,
  ExternalLink,
} from 'lucide-react';
import { dashboardApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { StatsCard } from '../components/dashboard/StatsCard';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();

  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: dashboardApi.getStats,
    refetchOnWindowFocus: true,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header & Greeting */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {user ? `Welcome back, ${user.name.split(' ')[0]}` : 'Candidate Dashboard'}
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Real-time analytics and ATS compatibility performance across all your evaluated roles.
          </p>
        </div>

        {/* Quick Action Buttons */}
        <div className="flex items-center gap-3">
          <Link
            to="/upload"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 shadow-xs hover:shadow transition-all"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Resume</span>
          </Link>

          <Link
            to="/jobs"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 shadow-2xs transition-all"
          >
            <Briefcase className="w-4 h-4 text-slate-500" />
            <span>New Analysis</span>
          </Link>
        </div>
      </div>

      {/* Guest Notice if not logged in */}
      {!user && (
        <div className="p-4 rounded-2xl bg-amber-50/80 border border-amber-200/80 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div className="flex-1 text-xs text-amber-800 space-y-1">
            <p className="font-semibold text-sm">Guest Session Active</p>
            <p>
              You are currently viewing analysis records associated with your temporary browser session.
              To retain permanent history across devices and unlock multiple role benchmarks,{' '}
              <Link to="/register" className="font-bold underline text-amber-900">
                create a free account
              </Link>
              .
            </p>
          </div>
        </div>
      )}

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatsCard
          title="Resumes Uploaded"
          value={isLoading ? '...' : stats?.total_resumes ?? 0}
          subtitle="Processed in database"
          icon={<FileText className="w-5 h-5" />}
          colorScheme="blue"
        />

        <StatsCard
          title="Analyses Performed"
          value={isLoading ? '...' : stats?.total_analyses ?? 0}
          subtitle="Multi-factor job audits"
          icon={<BarChart3 className="w-5 h-5" />}
          colorScheme="indigo"
        />

        <StatsCard
          title="Highest ATS Score"
          value={isLoading ? '...' : `${stats?.highest_ats_score?.toFixed(1) ?? '0.0'}%`}
          subtitle="Top matching qualification"
          icon={<Award className="w-5 h-5" />}
          colorScheme="emerald"
        />

        <StatsCard
          title="Average Compatibility"
          value={isLoading ? '...' : `${stats?.average_ats_score?.toFixed(1) ?? '0.0'}%`}
          subtitle="Overall candidate baseline"
          icon={<TrendingUp className="w-5 h-5" />}
          colorScheme="amber"
        />
      </div>

      {/* Main Content Grid: Recent Activity & Roles */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Recent Analyses */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Recent Analysis Records</h2>
              <p className="text-xs text-slate-500">Evaluated against verified job descriptions</p>
            </div>
            <Link
              to="/compare"
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
            >
              <span>Compare All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {isLoading ? (
            <div className="p-8 text-center text-slate-400 text-sm">Loading activity records...</div>
          ) : !stats?.recent_activity || stats.recent_activity.length === 0 ? (
            <div className="p-12 text-center border-2 border-dashed border-slate-200 rounded-xl space-y-3">
              <div className="w-12 h-12 rounded-xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
                <FileText className="w-6 h-6" />
              </div>
              <p className="text-sm font-semibold text-slate-700">No analyses performed yet</p>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Upload your resume and paste a job description or choose a preconfigured role to get your first ATS score.
              </p>
              <Link
                to="/upload"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors"
              >
                <Upload className="w-3.5 h-3.5" />
                Upload Resume Now
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-100 text-slate-400 uppercase font-semibold">
                    <th className="pb-3 font-semibold">Target Position</th>
                    <th className="pb-3 font-semibold">Resume File</th>
                    <th className="pb-3 font-semibold text-center">Score</th>
                    <th className="pb-3 font-semibold">Match Category</th>
                    <th className="pb-3 font-semibold text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {stats.recent_activity.map((item) => {
                    const score = item.ats_score;
                    const badgeColor =
                      score >= 85
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                        : score >= 70
                        ? 'bg-blue-50 text-blue-700 border-blue-200'
                        : score >= 50
                        ? 'bg-amber-50 text-amber-700 border-amber-200'
                        : 'bg-rose-50 text-rose-700 border-rose-200';

                    return (
                      <tr key={item.analysis_id} className="hover:bg-slate-50/70 transition-colors">
                        <td className="py-3.5 font-medium text-slate-800">
                          {item.job_title}
                          {item.company_name && (
                            <span className="block text-[10px] text-slate-400">{item.company_name}</span>
                          )}
                        </td>
                        <td className="py-3.5 text-slate-500 max-w-[140px] truncate">
                          {item.resume_filename}
                        </td>
                        <td className="py-3.5 text-center font-bold text-slate-900 text-sm">
                          {item.ats_score.toFixed(1)}%
                        </td>
                        <td className="py-3.5">
                          <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${badgeColor}`}>
                            {item.score_category}
                          </span>
                        </td>
                        <td className="py-3.5 text-right">
                          <Link
                            to={`/analysis/${item.analysis_id}`}
                            className="inline-flex items-center gap-1 font-semibold text-blue-600 hover:text-blue-700 hover:underline"
                          >
                            <span>View</span>
                            <ArrowRight className="w-3 h-3" />
                          </Link>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Right 1 Col: Quick Roles & Shortcuts */}
        <div className="space-y-6">
          {/* Recent Roles Analysed */}
          <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs">
            <h3 className="text-sm font-bold text-slate-900 mb-3">Recently Analyzed Roles</h3>
            {stats?.recent_roles_analyzed && stats.recent_roles_analyzed.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {stats.recent_roles_analyzed.map((role) => (
                  <span
                    key={role}
                    className="px-3 py-1 rounded-lg bg-slate-100 text-slate-700 text-xs font-medium border border-slate-200/60"
                  >
                    {role}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500">No roles analyzed yet.</p>
            )}

            <div className="mt-6 pt-4 border-t border-slate-100">
              <Link
                to="/jobs"
                className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center justify-between group"
              >
                <span>Browse all Job Templates</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>

          {/* Quick Start Card */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50/60 rounded-2xl border border-blue-100 p-6">
            <h4 className="text-sm font-bold text-slate-900">Compare Across Opportunities</h4>
            <p className="text-xs text-slate-600 mt-1 leading-relaxed">
              Have you applied to multiple positions? Compare compatibility, skill coverage, and keyword alignment across all roles.
            </p>
            <Link
              to="/compare"
              className="mt-4 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors shadow-2xs"
            >
              <GitCompare className="w-3.5 h-3.5" />
              Open Comparison Matrix
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

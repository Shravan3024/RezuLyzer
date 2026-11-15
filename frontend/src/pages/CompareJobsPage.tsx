import React, { useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  GitCompare,
  FileText,
  Briefcase,
  ArrowRight,
  TrendingUp,
  CheckCircle2,
  XCircle,
  ExternalLink,
  SlidersHorizontal,
} from 'lucide-react';
import { resumesApi, analysisApi } from '../services/api';

export const CompareJobsPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialResumeId = searchParams.get('resume_id');

  const [selectedResumeId, setSelectedResumeId] = useState<string>(initialResumeId || '');

  // Fetch resumes list
  const { data: resumesList } = useQuery({
    queryKey: ['resumes-list'],
    queryFn: resumesApi.getAll,
  });

  // Automatically select first resume if none set
  React.useEffect(() => {
    if (!selectedResumeId && resumesList && resumesList.length > 0) {
      setSelectedResumeId(resumesList[0].id);
    }
  }, [resumesList, selectedResumeId]);

  // Fetch multi-job comparison for this resume
  const { data: comparisonData, isLoading, error } = useQuery({
    queryKey: ['compare-jobs', selectedResumeId],
    queryFn: () => analysisApi.compareMultipleJobs({ resume_id: selectedResumeId }),
    enabled: !!selectedResumeId,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Header */}
      <div>
        <div className="flex items-center gap-2">
          <GitCompare className="w-6 h-6 text-blue-600" />
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Multi-Role Comparison Dashboard
          </h1>
        </div>
        <p className="text-sm text-slate-500 mt-1">
          Evaluate how your single resume performs across different target roles, skill requirements, and ATS models.
        </p>
      </div>

      {/* Resume Selection Selector */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs uppercase font-bold text-slate-400">Comparing Opportunities For:</span>
            <div className="flex items-center gap-2 mt-0.5">
              {resumesList && resumesList.length > 0 ? (
                <select
                  value={selectedResumeId}
                  onChange={(e) => setSelectedResumeId(e.target.value)}
                  className="text-sm font-semibold text-slate-900 bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-blue-500 outline-hidden"
                >
                  {resumesList.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.filename} ({r.file_type.toUpperCase()})
                    </option>
                  ))}
                </select>
              ) : (
                <span className="text-sm text-rose-600 font-medium">No resumes found. Please upload one first.</span>
              )}
            </div>
          </div>
        </div>

        {selectedResumeId && (
          <Link
            to={`/jobs?resume_id=${selectedResumeId}`}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 transition-colors"
          >
            <Briefcase className="w-3.5 h-3.5" />
            <span>Analyze Additional Role</span>
          </Link>
        )}
      </div>

      {/* Comparison Results */}
      {isLoading ? (
        <div className="bg-white rounded-2xl p-12 text-center text-slate-400 text-sm border border-slate-200/80">
          Loading multi-job comparison records...
        </div>
      ) : !comparisonData || comparisonData.comparisons.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-xs space-y-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto">
            <GitCompare className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">No Job Analyses for this Resume</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            To compare multiple opportunities, run analysis for this resume against at least one or two job postings.
          </p>
          <Link
            to={selectedResumeId ? `/jobs?resume_id=${selectedResumeId}` : '/upload'}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 transition-colors shadow-2xs"
          >
            <span>Analyze Job for this Resume</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Quick Summary Pill */}
          <div className="flex items-center justify-between text-xs text-slate-500 px-1">
            <span>
              Benchmarking <strong>{comparisonData.total_compared}</strong> opportunities for{' '}
              <strong className="text-slate-800">{comparisonData.resume_filename}</strong>
            </span>
            <span className="text-slate-400">Sorted by Highest Compatibility Score</span>
          </div>

          {/* Comparison Cards / Table */}
          <div className="grid grid-cols-1 gap-4">
            {comparisonData.comparisons.map((item, idx) => {
              const score = item.ats_score;
              const badgeBg =
                score >= 85
                  ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                  : score >= 70
                  ? 'bg-blue-50 text-blue-800 border-blue-200'
                  : score >= 50
                  ? 'bg-amber-50 text-amber-800 border-amber-200'
                  : 'bg-rose-50 text-rose-800 border-rose-200';

              return (
                <div
                  key={item.analysis_id}
                  className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs hover:border-blue-300 transition-all flex flex-col lg:flex-row lg:items-center justify-between gap-6"
                >
                  {/* Left: Job & Category */}
                  <div className="space-y-1.5 min-w-[240px]">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-full bg-slate-100 text-slate-700 font-bold text-xs flex items-center justify-center">
                        #{idx + 1}
                      </span>
                      <h3 className="text-lg font-bold text-slate-900">{item.job_title}</h3>
                    </div>
                    {item.company_name && (
                      <p className="text-xs text-slate-500 pl-8">{item.company_name}</p>
                    )}
                    <div className="pl-8 pt-1 flex items-center gap-2">
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${badgeBg}`}>
                        {item.score_category}
                      </span>
                      <span className="text-[11px] text-slate-400">
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  {/* Middle: Metrics Matrix */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 flex-1">
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">ATS Score</span>
                      <span className="text-xl font-extrabold text-slate-900">
                        {item.ats_score.toFixed(1)}%
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">Skills Coverage</span>
                      <span className="text-xl font-extrabold text-blue-600">
                        {item.required_skills_coverage.toFixed(1)}%
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">Semantic Sim.</span>
                      <span className="text-xl font-extrabold text-indigo-600">
                        {item.semantic_similarity.toFixed(1)}%
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">Experience</span>
                      <span className="text-xs font-semibold text-slate-700 block truncate mt-1">
                        {item.experience_match}
                      </span>
                    </div>
                  </div>

                  {/* Right: Actions */}
                  <div className="flex sm:flex-col items-center justify-end gap-2 shrink-0">
                    <Link
                      to={`/analysis/${item.analysis_id}`}
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 transition-colors shadow-2xs"
                    >
                      <span>View Full Audit</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

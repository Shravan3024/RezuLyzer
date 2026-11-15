import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  FileText,
  Download,
  Share2,
  GitCompare,
  ArrowRight,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Layers,
  Search,
  User,
  GraduationCap,
  Briefcase,
  Sliders,
  Sparkles,
  Info,
  Calendar,
  Building,
  Check,
} from 'lucide-react';
import { analysisApi } from '../services/api';
import { CircularProgress } from '../components/common/CircularProgress';
import { ScoreBreakdownChart } from '../components/analysis/ScoreBreakdownChart';
import { SkillPill } from '../components/analysis/SkillPill';

export const AnalysisResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [isDownloading, setIsDownloading] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);

  const { data: analysis, isLoading, error } = useQuery({
    queryKey: ['analysis-result', id],
    queryFn: () => analysisApi.getById(id!),
    enabled: !!id,
  });

  const handleDownloadPdf = async () => {
    if (!analysis) return;
    setIsDownloading(true);
    try {
      await analysisApi.downloadReport(
        analysis.id,
        `ResuLyzer_Audit_${analysis.job_title?.replace(/[\s/]/g, '_') || 'Report'}.pdf`
      );
    } catch (err) {
      alert('Failed to generate PDF report. Please try again.');
    } finally {
      setIsDownloading(false);
    }
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2500);
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mx-auto animate-pulse">
          <Sparkles className="w-6 h-6 animate-spin" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Loading Analysis Results...</h2>
        <p className="text-xs text-slate-500">Retrieving mathematical model metrics and skill matrices.</p>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center mx-auto">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Analysis Not Found</h2>
        <p className="text-xs text-slate-500">
          The requested audit record may have expired or been deleted.
        </p>
        <Link
          to="/upload"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700"
        >
          <span>Start New Analysis</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  const score = analysis.ats_score;
  const categoryLabel =
    score >= 85
      ? 'Strong Match'
      : score >= 70
      ? 'Good Match'
      : score >= 50
      ? 'Moderate Match'
      : 'Low Match';

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Banner / Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-slate-200 gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              {analysis.job_title}
            </h1>
            <span className="text-xs uppercase font-bold px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
              Audit Report
            </span>
          </div>
          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mt-1.5">
            {analysis.company_name && (
              <span className="flex items-center gap-1 font-medium text-slate-700">
                <Building className="w-3.5 h-3.5 text-slate-400" />
                {analysis.company_name}
              </span>
            )}
            <span className="flex items-center gap-1">
              <FileText className="w-3.5 h-3.5 text-slate-400" />
              {analysis.resume_filename}
            </span>
            <span className="flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              {new Date(analysis.created_at).toLocaleString()}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleShare}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 shadow-2xs transition-all"
          >
            {copiedLink ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Share2 className="w-3.5 h-3.5" />}
            <span>{copiedLink ? 'Link Copied' : 'Share'}</span>
          </button>

          <Link
            to={`/compare?resume_id=${analysis.resume_id}`}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 shadow-2xs transition-all"
          >
            <GitCompare className="w-3.5 h-3.5 text-slate-500" />
            <span>Compare Other Roles</span>
          </Link>

          <button
            onClick={handleDownloadPdf}
            disabled={isDownloading}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-xs hover:shadow transition-all disabled:opacity-50"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{isDownloading ? 'Generating PDF...' : 'Download PDF Audit'}</span>
          </button>
        </div>
      </div>

      {/* SECTION A: Overall ATS Compatibility & Primary Gauge */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-xs">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
          {/* Circular Progress Gauge */}
          <div className="flex justify-center border-b lg:border-b-0 lg:border-r border-slate-100 pb-6 lg:pb-0 lg:pr-6">
            <CircularProgress
              score={analysis.ats_score}
              category={categoryLabel}
              label="Overall ATS Score"
            />
          </div>

          {/* Score Explanation & High-level stats */}
          <div className="lg:col-span-2 space-y-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs uppercase font-bold text-blue-600 tracking-wider">
                  Compatibility Assessment
                </span>
              </div>
              <h2 className="text-xl font-bold text-slate-900 mt-1">
                {categoryLabel}: {analysis.ats_score.toFixed(1)}% Match
              </h2>
              <p className="text-sm text-slate-600 mt-2 leading-relaxed">
                {score >= 85
                  ? 'Your resume shows exceptional alignment with the stated requirements, core technical stack, and responsibilities for this opportunity.'
                  : score >= 70
                  ? 'Your background demonstrates solid alignment with core qualifications. Targeted adjustments to missing skills and keywords can elevate your candidate profile to the top tier.'
                  : score >= 50
                  ? 'Your resume possesses foundational qualifications, but key gaps in required proficiencies or experience tenure reduce automated ATS ranking.'
                  : 'Noticeable divergence exists between your current resume content and the primary qualifications expected for this position.'}
              </p>
            </div>

            {/* Quick Metrics Bar */}
            <div className="grid grid-cols-3 gap-3 pt-2">
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Matched Skills</span>
                <span className="text-lg font-extrabold text-slate-900">
                  {analysis.matched_skills?.length || 0}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Missing Core Skills</span>
                <span className="text-lg font-extrabold text-rose-600">
                  {analysis.missing_skills?.required?.length || 0}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Semantic Sim.</span>
                <span className="text-lg font-extrabold text-indigo-600">
                  {analysis.semantic_similarity?.toFixed(1) || 0}%
                </span>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="flex items-start gap-2 pt-2 text-[11px] text-slate-400">
              <Info className="w-3.5 h-3.5 shrink-0 mt-0.5 text-slate-400" />
              <span>
                This compatibility score is calculated using ResuLyzer's multi-factor NLP matching engine. It is an objective analytical estimate, not an official rating issued by the employer.
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* SECTION B: Component Breakdown Chart */}
      <ScoreBreakdownChart breakdown={analysis.score_breakdown} />

      {/* SECTION C & D: Matched Skills and Missing Skills */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Matched Skills */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
              <h3 className="text-base font-bold text-slate-900">
                Matched Skills ({analysis.matched_skills?.length || 0})
              </h3>
            </div>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
              Verified in Resume
            </span>
          </div>

          <p className="text-xs text-slate-500">
            Skills identified in both your resume and the job requirements:
          </p>

          <div className="flex flex-wrap gap-2 pt-1">
            {analysis.matched_skills && analysis.matched_skills.length > 0 ? (
              analysis.matched_skills.map((s, idx) => (
                <SkillPill
                  key={`${s.skill || s.name}-${idx}`}
                  name={s.skill || s.name}
                  category={s.category}
                  type="matched"
                  matchedAs={s.matched_as}
                />
              ))
            ) : (
              <p className="text-xs text-slate-400">No overlapping skills explicitly detected.</p>
            )}
          </div>
        </div>

        {/* Missing Skills */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <XCircle className="w-5 h-5 text-rose-600" />
              <h3 className="text-base font-bold text-slate-900">
                Missing Skill Gaps
              </h3>
            </div>
            <span className="text-xs font-semibold text-rose-700 bg-rose-50 px-2 py-0.5 rounded-full border border-rose-200">
              Needs Attention
            </span>
          </div>

          {/* Missing Required Skills */}
          <div>
            <span className="text-xs font-bold text-slate-700 block mb-2">
              Required Skills Missing from Resume ({analysis.missing_skills?.required?.length || 0})
            </span>
            <div className="flex flex-wrap gap-2">
              {analysis.missing_skills?.required && analysis.missing_skills.required.length > 0 ? (
                analysis.missing_skills.required.map((s) => (
                  <SkillPill key={s} name={s} type="missing_required" />
                ))
              ) : (
                <p className="text-xs text-emerald-600 font-semibold">
                  All mandatory required skills were detected in your resume!
                </p>
              )}
            </div>
          </div>

          {/* Missing Preferred Skills */}
          {analysis.missing_skills?.preferred && analysis.missing_skills.preferred.length > 0 && (
            <div className="pt-2 border-t border-slate-100">
              <span className="text-xs font-bold text-slate-600 block mb-2">
                Secondary / Preferred Skills Missing ({analysis.missing_skills.preferred.length})
              </span>
              <div className="flex flex-wrap gap-2">
                {analysis.missing_skills.preferred.map((s) => (
                  <SkillPill key={s} name={s} type="missing_preferred" />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* SECTION E: Keyword Frequency & Coverage Analysis */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Search className="w-5 h-5 text-blue-600" />
            <h3 className="text-base font-bold text-slate-900">Keyword Coverage & Density</h3>
          </div>
          <span className="text-xs font-bold text-blue-700 bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
            {analysis.keyword_analysis?.keyword_coverage_pct?.toFixed(1) || 0}% Job Keyword Coverage
          </span>
        </div>

        <p className="text-xs text-slate-500">
          Evaluates how thoroughly your resume incorporates specific domain terminology found in the posting.
        </p>

        {analysis.keyword_analysis?.matched_keywords && analysis.keyword_analysis.matched_keywords.length > 0 && (
          <div className="overflow-x-auto pt-2">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 font-semibold uppercase">
                  <th className="pb-2 font-semibold">Matched Keyword</th>
                  <th className="pb-2 font-semibold text-center">Frequency in Resume</th>
                  <th className="pb-2 font-semibold text-center">Frequency in Job Posting</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {analysis.keyword_analysis.matched_keywords.slice(0, 10).map((kw, i) => (
                  <tr key={i} className="hover:bg-slate-50/60">
                    <td className="py-2.5 font-semibold text-slate-800 capitalize">{kw.keyword}</td>
                    <td className="py-2.5 text-center font-bold text-blue-600">{kw.frequency_in_resume}x</td>
                    <td className="py-2.5 text-center text-slate-500">{kw.frequency_in_job}x</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Missing Keywords Badges */}
        {analysis.keyword_analysis?.missing_keywords && analysis.keyword_analysis.missing_keywords.length > 0 && (
          <div className="pt-3 border-t border-slate-100">
            <span className="text-xs font-bold text-slate-600 block mb-2">
              Salient Job Keywords Absent in Resume:
            </span>
            <div className="flex flex-wrap gap-1.5">
              {analysis.keyword_analysis.missing_keywords.slice(0, 15).map((kw) => (
                <span
                  key={kw}
                  className="px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-700 text-xs font-medium"
                >
                  {kw}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* SECTION G & H: Experience & Education Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Experience Analysis */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <div className="flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-blue-600" />
            <h3 className="text-base font-bold text-slate-900">Experience Alignment</h3>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-500">Required Tenure:</span>
              <span className="font-bold text-slate-900">
                {analysis.experience_analysis?.required_years
                  ? `${analysis.experience_analysis.required_years}+ years`
                  : 'Entry Level / Unspecified'}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-500">Detected Candidate Tenure:</span>
              <span className="font-bold text-blue-600">
                {analysis.experience_analysis?.candidate_years !== null &&
                analysis.experience_analysis?.candidate_years !== undefined
                  ? `~${analysis.experience_analysis.candidate_years} years`
                  : 'Unable to determine'}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-200/60">
              <span className="text-slate-500">Tenure Score:</span>
              <span className="font-bold text-emerald-600 text-sm">
                {analysis.experience_analysis?.score?.toFixed(1) || 0} / 100
              </span>
            </div>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed">
            {analysis.experience_analysis?.explanation}
          </p>
        </div>

        {/* Education Analysis */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
          <div className="flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-blue-600" />
            <h3 className="text-base font-bold text-slate-900">Education & Degree Level</h3>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-500">Job Expectation:</span>
              <span className="font-bold text-slate-900">
                {analysis.education_analysis?.required_level || 'Flexible'}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-500">Candidate Highest Credential:</span>
              <span className="font-bold text-blue-600">
                {analysis.education_analysis?.candidate_highest_level || 'Unspecified'}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-200/60">
              <span className="text-slate-500">Education Score:</span>
              <span className="font-bold text-emerald-600 text-sm">
                {analysis.education_analysis?.score?.toFixed(1) || 0} / 100
              </span>
            </div>
          </div>

          <p className="text-xs text-slate-600 leading-relaxed">
            {analysis.education_analysis?.explanation}
          </p>
        </div>
      </div>

      {/* SECTION I: Resume Structure Completeness */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sliders className="w-5 h-5 text-blue-600" />
            <h3 className="text-base font-bold text-slate-900">Resume Structure & Parsing Readability</h3>
          </div>
          <span className="text-xs font-bold text-slate-700 bg-slate-100 px-3 py-1 rounded-full">
            {analysis.structure_analysis?.score?.toFixed(1) || 0} / 100 Struct Score
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
          {[
            { label: 'Contact Details', ok: analysis.structure_analysis?.has_contact_info },
            { label: 'Summary Section', ok: analysis.structure_analysis?.has_summary },
            { label: 'Skills Section', ok: analysis.structure_analysis?.has_skills },
            { label: 'Experience Section', ok: analysis.structure_analysis?.has_experience },
            { label: 'Projects Section', ok: analysis.structure_analysis?.has_projects },
          ].map((item, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-xl border flex items-center justify-between text-xs ${
                item.ok ? 'bg-emerald-50/50 border-emerald-200 text-emerald-900' : 'bg-slate-50 border-slate-200 text-slate-500'
              }`}
            >
              <span className="font-semibold">{item.label}</span>
              {item.ok ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              ) : (
                <span className="text-[10px] text-slate-400 font-bold uppercase">Missing</span>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* SECTION J: Actionable Improvement Recommendations */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-xs space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-slate-900">
              Actionable Improvement Recommendations ({analysis.recommendations?.length || 0})
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Targeted, factual enhancements based on your specific audit gaps
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {analysis.recommendations && analysis.recommendations.length > 0 ? (
            analysis.recommendations.map((rec, i) => {
              const p = rec.priority?.toLowerCase();
              const badgeStyle =
                p === 'high'
                  ? 'bg-rose-50 text-rose-700 border-rose-200'
                  : p === 'medium'
                  ? 'bg-blue-50 text-blue-700 border-blue-200'
                  : 'bg-emerald-50 text-emerald-700 border-emerald-200';

              return (
                <div
                  key={i}
                  className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-blue-200 transition-all space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-slate-900">{rec.title}</span>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] uppercase font-bold border ${badgeStyle}`}>
                      {rec.priority} Priority
                    </span>
                  </div>

                  <p className="text-xs text-slate-600 leading-relaxed">{rec.description}</p>

                  <div className="pt-2 flex items-center gap-1.5 text-xs text-blue-700 font-semibold">
                    <ArrowRight className="w-3.5 h-3.5" />
                    <span>Recommended Action: {rec.action}</span>
                  </div>
                </div>
              );
            })
          ) : (
            <p className="text-xs text-slate-400">No major recommendations generated.</p>
          )}
        </div>
      </div>

      {/* Bottom Action Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between p-6 bg-slate-900 rounded-2xl text-white gap-4">
        <div>
          <h4 className="text-sm font-bold">Ready to compare with other roles?</h4>
          <p className="text-xs text-slate-400 mt-0.5">
            You can analyze this same resume against multiple target job postings without re-uploading.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to={`/jobs?resume_id=${analysis.resume_id}`}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-200 bg-slate-800 hover:bg-slate-700 transition-colors"
          >
            Analyze Another Job
          </Link>
          <Link
            to={`/compare?resume_id=${analysis.resume_id}`}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 transition-colors"
          >
            View Multi-Job Comparison
          </Link>
        </div>
      </div>
    </div>
  );
};

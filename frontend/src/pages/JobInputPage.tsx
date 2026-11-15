import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Briefcase,
  FileText,
  Search,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Sliders,
  Layers,
  Building,
} from 'lucide-react';
import { jobsApi, resumesApi, analysisApi } from '../services/api';
import { JobTemplate, Resume } from '../types';

export const JobInputPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const preselectedResumeId = searchParams.get('resume_id');

  const [mode, setMode] = useState<'paste' | 'template'>('paste');
  const [selectedResumeId, setSelectedResumeId] = useState<string>(preselectedResumeId || '');

  // Mode 1: Paste fields
  const [jobTitle, setJobTitle] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [descriptionText, setDescriptionText] = useState('');

  // Mode 2: Template selection & customization
  const [selectedRoleName, setSelectedRoleName] = useState('');
  const [customReqs, setCustomReqs] = useState<any>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  // Submit loading state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  // Queries
  const { data: resumesList } = useQuery({
    queryKey: ['resumes-list'],
    queryFn: resumesApi.getAll,
  });

  const { data: templates } = useQuery({
    queryKey: ['job-templates'],
    queryFn: jobsApi.getTemplates,
  });

  // Set default resume if only one exists or preselected
  useEffect(() => {
    if (preselectedResumeId) {
      setSelectedResumeId(preselectedResumeId);
    } else if (resumesList && resumesList.length > 0 && !selectedResumeId) {
      setSelectedResumeId(resumesList[0].id);
    }
  }, [resumesList, preselectedResumeId]);

  // When a template is clicked
  const handleSelectTemplate = (template: JobTemplate) => {
    setSelectedRoleName(template.role_name);
    setJobTitle(template.role_name);
    setDescriptionText(template.description);
    setCustomReqs(template.requirements);
  };

  const categories = ['All', ...Array.from(new Set(templates?.map((t) => t.category) || []))];

  const filteredTemplates = templates?.filter((t) => {
    if (selectedCategory === 'All') return true;
    return t.category === selectedCategory;
  });

  const handleStartAnalysis = async () => {
    if (!selectedResumeId) {
      setSubmitError('Please select or upload a resume to analyze.');
      return;
    }

    if (mode === 'paste') {
      if (!jobTitle.trim()) {
        setSubmitError('Please enter a job title.');
        return;
      }
      if (!descriptionText.trim() || descriptionText.trim().length < 20) {
        setSubmitError('Please provide a substantive job description (at least 20 characters).');
        return;
      }
    } else {
      if (!selectedRoleName) {
        setSubmitError('Please choose a job role template or enter a target title.');
        return;
      }
    }

    setSubmitError(null);
    setIsSubmitting(true);

    try {
      const payload: any = {
        resume_id: selectedResumeId,
        source_type: mode === 'paste' ? 'pasted' : 'template',
      };

      if (mode === 'paste') {
        payload.job_title = jobTitle.trim();
        payload.company_name = companyName.trim() || undefined;
        payload.job_description_text = descriptionText.trim();
      } else {
        payload.job_title = selectedRoleName;
        payload.template_role_name = selectedRoleName;
        payload.job_description_text = descriptionText;
        payload.custom_requirements = customReqs;
      }

      // Navigate to loading screen with state, or perform analysis directly
      const result = await analysisApi.analyze(payload);
      navigate(`/analysis/${result.id}`);
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Analysis failed. Please check inputs and try again.';
      setSubmitError(msg);
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Heading */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Job Opportunity Analysis
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Select an active resume and specify the job requirements through a pasted posting or curated role profile.
        </p>
      </div>

      {/* Resume Selection Bar */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs uppercase font-bold text-slate-400">Target Candidate Resume</span>
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
                <span className="text-sm text-rose-600 font-medium">No resumes uploaded yet</span>
              )}
            </div>
          </div>
        </div>

        <Link
          to="/upload"
          className="text-xs font-semibold text-blue-600 hover:text-blue-700 underline underline-offset-2 flex items-center gap-1"
        >
          <span>Upload Different Resume</span>
        </Link>
      </div>

      {/* Mode Switcher Tabs */}
      <div className="flex border-b border-slate-200 gap-8 text-sm font-medium">
        <button
          onClick={() => setMode('paste')}
          className={`pb-3.5 transition-colors relative font-semibold ${
            mode === 'paste' ? 'text-blue-600' : 'text-slate-500 hover:text-slate-800'
          }`}
        >
          Mode 1: Paste Job Description
          {mode === 'paste' && (
            <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 rounded-t-full" />
          )}
        </button>

        <button
          onClick={() => setMode('template')}
          className={`pb-3.5 transition-colors relative font-semibold flex items-center gap-1.5 ${
            mode === 'template' ? 'text-blue-600' : 'text-slate-500 hover:text-slate-800'
          }`}
        >
          <Sparkles className="w-4 h-4 text-blue-600" />
          Mode 2: Job Role & Profile Templates
          {mode === 'template' && (
            <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 rounded-t-full" />
          )}
        </button>
      </div>

      {/* Mode 1: Paste Job Description */}
      {mode === 'paste' && (
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-xs space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-1">
                Job Title <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                placeholder="e.g. Senior Full Stack Engineer, Financial Analyst, Mechanical Design Lead"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-blue-500 outline-hidden"
              />
            </div>

            <div>
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-1">
                Company Name <span className="text-slate-400 font-normal">(Optional)</span>
              </label>
              <input
                type="text"
                placeholder="e.g. Google, Tesla, Stripe, Siemens"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:ring-2 focus:ring-blue-500 outline-hidden"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider block mb-1">
              Full Job Description <span className="text-rose-500">*</span>
            </label>
            <p className="text-xs text-slate-500 mb-2">
              Paste the complete job posting including responsibilities, required qualifications, and nice-to-have skills.
            </p>
            <textarea
              rows={12}
              placeholder="Paste job posting text here..."
              value={descriptionText}
              onChange={(e) => setDescriptionText(e.target.value)}
              className="w-full p-4 rounded-xl border border-slate-300 text-sm font-sans focus:ring-2 focus:ring-blue-500 outline-hidden"
            />
          </div>
        </div>
      )}

      {/* Mode 2: Role Based Analysis */}
      {mode === 'template' && (
        <div className="space-y-6">
          {/* Category Filter Pills */}
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white border-blue-600 shadow-2xs'
                    : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Templates Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredTemplates?.map((t) => {
              const isSelected = selectedRoleName === t.role_name;
              return (
                <div
                  key={t.id}
                  onClick={() => handleSelectTemplate(t)}
                  className={`p-5 rounded-2xl border transition-all cursor-pointer ${
                    isSelected
                      ? 'border-blue-600 bg-blue-50/70 ring-2 ring-blue-500/20 shadow-xs'
                      : 'border-slate-200/90 bg-white hover:border-blue-300 hover:shadow-xs'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-100 text-slate-700">
                      {t.category}
                    </span>
                    {isSelected && <CheckCircle2 className="w-4 h-4 text-blue-600" />}
                  </div>

                  <h3 className="text-base font-bold text-slate-900">{t.role_name}</h3>
                  <p className="text-xs text-slate-600 mt-1 line-clamp-2 leading-relaxed">
                    {t.description}
                  </p>

                  <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap gap-1.5">
                    {t.requirements?.required_skills?.slice(0, 4).map((s) => (
                      <span
                        key={s}
                        className="px-2 py-0.5 rounded-md bg-slate-100 text-[10px] font-semibold text-slate-700 capitalize"
                      >
                        {s}
                      </span>
                    ))}
                    {t.requirements?.required_skills?.length > 4 && (
                      <span className="text-[10px] text-slate-400 self-center">
                        +{t.requirements.required_skills.length - 4} more
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Selected Role Review & Edit Box */}
          {selectedRoleName && customReqs && (
            <div className="bg-white rounded-2xl border border-blue-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <h3 className="text-base font-bold text-slate-900">
                    Target Role: {selectedRoleName}
                  </h3>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-800 border border-amber-200 font-semibold">
                    Template Requirements
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/70 space-y-2">
                  <span className="font-bold text-slate-700 uppercase tracking-wider block">
                    Core Required Skills
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {customReqs.required_skills?.map((s: string) => (
                      <span
                        key={s}
                        className="px-2.5 py-1 rounded-full bg-blue-100 text-blue-800 font-semibold capitalize"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/70 space-y-2">
                  <span className="font-bold text-slate-700 uppercase tracking-wider block">
                    Preferred Qualifications
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {customReqs.preferred_skills?.map((s: string) => (
                      <span
                        key={s}
                        className="px-2.5 py-1 rounded-full bg-slate-200 text-slate-700 font-medium capitalize"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <p className="text-[11px] text-slate-500 italic">
                Note: Job template profiles represent industry benchmarks. You can customize them or compare against actual employer postings.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Submit Error Alert */}
      {submitError && (
        <div className="flex items-start gap-3 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">Unable to Proceed</p>
            <p className="text-xs text-rose-700 mt-0.5">{submitError}</p>
          </div>
        </div>
      )}

      {/* Action Footer */}
      <div className="flex items-center justify-end gap-4 pt-4 border-t border-slate-200">
        <Link
          to="/upload"
          className="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:text-slate-800"
        >
          Back to Resumes
        </Link>

        <button
          onClick={handleStartAnalysis}
          disabled={isSubmitting || !selectedResumeId}
          className="inline-flex items-center gap-2 px-8 py-3 rounded-xl font-bold text-sm text-white bg-blue-600 hover:bg-blue-700 shadow-sm hover:shadow transition-all disabled:opacity-50 disabled:pointer-events-none"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Running NLP Pipeline...</span>
            </>
          ) : (
            <>
              <span>Analyze Compatibility</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
};

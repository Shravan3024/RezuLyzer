import React from 'react';
import { Link } from 'react-router-dom';
import {
  FileText,
  Search,
  CheckCircle2,
  TrendingUp,
  ShieldCheck,
  GitCompare,
  ArrowRight,
  Brain,
  Layers,
  Sparkles,
  BarChart3,
  Sliders,
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="space-y-24 pb-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 sm:pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 mb-6 shadow-2xs">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            <span>AI-Driven Applicant Tracking System Audit</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-[1.15]">
            Your Resume Deserves More Than a <span className="text-blue-600">Guess</span>.
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Analyze your resume against any job opportunity using intelligent NLP-powered matching,
            ATS compatibility scoring, and actionable improvement recommendations.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/upload"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl text-base font-semibold text-white bg-blue-600 hover:bg-blue-700 shadow-md shadow-blue-500/20 hover:shadow-lg transition-all"
            >
              <FileText className="w-5 h-5" />
              <span>Analyze My Resume</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>

            <a
              href="#features"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 shadow-xs transition-all"
            >
              <span>Explore Features</span>
            </a>
          </div>

          {/* Quick credibility highlights */}
          <div className="mt-12 pt-8 border-t border-slate-200/60 max-w-3xl mx-auto flex flex-wrap items-center justify-center gap-6 sm:gap-12 text-xs font-medium text-slate-500">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Zero Hardcoded Scores
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Real spaCy & Transformer NLP
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Transparent Scoring Breakdown
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              100% Private Document Processing
            </span>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="text-xs uppercase font-bold text-blue-600 tracking-wider">
            Clear Four-Step Workflow
          </span>
          <h2 className="text-3xl font-extrabold text-slate-900 mt-2">How ResuLyzer Works</h2>
          <p className="text-sm text-slate-600 mt-2">
            No black-box mystery. Our NLP pipeline dissects your qualifications and maps them directly to employer criteria.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            {
              step: '01',
              title: 'Upload Resume',
              desc: 'Upload any standard PDF or DOCX file. Our engine parses sections, contact details, education, and skills.',
              icon: <FileText className="w-6 h-6 text-blue-600" />,
            },
            {
              step: '02',
              title: 'Add Job Description',
              desc: 'Paste a specific job posting or select an editable industry profile across engineering, marketing, finance, or tech.',
              icon: <Search className="w-6 h-6 text-blue-600" />,
            },
            {
              step: '03',
              title: 'Get Intelligent Analysis',
              desc: 'Our engine computes exact keyword matches, TF-IDF cosine similarity, dense embeddings, and tenure alignments.',
              icon: <Brain className="w-6 h-6 text-blue-600" />,
            },
            {
              step: '04',
              title: 'Improve Your Resume',
              desc: 'Review missing skills, keyword frequency gaps, structural advice, and export a downloadable PDF audit report.',
              icon: <TrendingUp className="w-6 h-6 text-blue-600" />,
            },
          ].map((item) => (
            <div
              key={item.step}
              className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow relative"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center border border-blue-100">
                  {item.icon}
                </div>
                <span className="text-2xl font-black text-slate-200">{item.step}</span>
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-1.5">{item.title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="text-xs uppercase font-bold text-blue-600 tracking-wider">
            Engineered Capabilities
          </span>
          <h2 className="text-3xl font-extrabold text-slate-900 mt-2">Comprehensive Analysis Suite</h2>
          <p className="text-sm text-slate-600 mt-2">
            Every feature is backed by real mathematical modeling, information retrieval algorithms, and natural language processing.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              title: 'AI Resume Parsing',
              desc: 'Extracts contact details, work history, degree hierarchies, technical proficiencies, and project portfolios accurately from PDF and DOCX documents.',
              icon: <FileText className="w-6 h-6 text-blue-600" />,
            },
            {
              title: 'ATS Compatibility Score',
              desc: 'Weighted 0–100 scoring based on required skills (35%), semantic similarity (25%), keywords (15%), experience (10%), education (10%), and structure (5%).',
              icon: <BarChart3 className="w-6 h-6 text-indigo-600" />,
            },
            {
              title: 'Skill Gap Detection',
              desc: 'Identifies missing required competencies vs preferred skills using an extensive taxonomy of aliases, synonyms, and multi-word phrase matching.',
              icon: <Layers className="w-6 h-6 text-cyan-600" />,
            },
            {
              title: 'Semantic Matching',
              desc: 'Employs Sentence Transformers (all-MiniLM-L6-v2) for contextual semantic understanding, with reliable TF-IDF vectorization fallback.',
              icon: <Brain className="w-6 h-6 text-purple-600" />,
            },
            {
              title: 'Actionable Recommendations',
              desc: 'Provides constructive, non-hallucinatory guidance to highlight verified qualifications, quantify achievements, and format dates for ATS scanners.',
              icon: <Sliders className="w-6 h-6 text-amber-600" />,
            },
            {
              title: 'Multi-Role Comparison',
              desc: 'Upload a resume once and benchmark it simultaneously across multiple target positions to determine where your candidate profile matches strongest.',
              icon: <GitCompare className="w-6 h-6 text-emerald-600" />,
            },
          ].map((f) => (
            <div
              key={f.title}
              className="bg-white rounded-2xl p-7 border border-slate-200/80 shadow-xs hover:border-blue-200 transition-all"
            >
              <div className="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center border border-slate-100 mb-5">
                {f.icon}
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-2">{f.title}</h3>
              <p className="text-sm text-slate-600 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Why ResuLyzer Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 rounded-3xl p-8 sm:p-14 text-white shadow-xl">
          <div className="max-w-3xl">
            <span className="text-xs uppercase font-bold text-blue-300 tracking-wider">
              Transparent & Objective
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold mt-3 tracking-tight">
              Why Professionals Choose ResuLyzer
            </h2>
            <p className="mt-4 text-base text-blue-100 leading-relaxed">
              Traditional resume tools give you arbitrary percentages with no mathematical justification.
              ResuLyzer discloses the exact weights, matched tokens, missing skills, and cosine distances so you can optimize with complete confidence.
            </p>

            <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <p className="text-sm text-blue-100">
                  <strong>Non-Hallucinatory:</strong> We never invent fake jobs, degrees, or certifications.
                </p>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <p className="text-sm text-blue-100">
                  <strong>Universal Coverage:</strong> Evaluates IT, finance, management, and core engineering roles.
                </p>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <p className="text-sm text-blue-100">
                  <strong>No Account Required:</strong> Try full analysis immediately with guest session storage.
                </p>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <p className="text-sm text-blue-100">
                  <strong>Audit Report PDF:</strong> Download a clean, recruiter-ready report of your analysis.
                </p>
              </div>
            </div>

            <div className="mt-10">
              <Link
                to="/upload"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-blue-900 bg-white hover:bg-blue-50 shadow-md transition-all text-sm"
              >
                <span>Start Free Analysis</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};


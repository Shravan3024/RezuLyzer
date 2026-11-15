import React from 'react';
import { FileText, CheckCircle2, AlertTriangle } from 'lucide-react';

export const TermsPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Terms of Service</h1>
        <p className="text-sm text-slate-500 mt-1">Last Updated: November 2026</p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-xs space-y-6 text-sm text-slate-700 leading-relaxed">
        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900">1. Acceptance of Terms</h2>
          <p>
            By accessing or using ResuLyzer, you agree to comply with and be bound by these Terms of Service.
            If you do not agree with any part of these terms, you should discontinue use of the platform.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900">2. Algorithmic Scoring Disclaimer</h2>
          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs space-y-1">
            <p className="font-bold flex items-center gap-1.5 text-sm">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              Important Notice on ATS Scores
            </p>
            <p>
              ResuLyzer provides an objective mathematical assessment based on document parsing, keyword coverage, and semantic similarity.
              The ATS compatibility score is an informational estimate designed to guide your self-improvement. It does not represent an endorsement,
              official score, or guarantee of employment by any specific employer or proprietary Applicant Tracking System.
            </p>
          </div>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900">3. User Conduct & Accuracy</h2>
          <p>
            Users are solely responsible for the authenticity and truthfulness of the documents they upload.
            ResuLyzer encourages candidates to truthfully represent their qualifications and never fabricate credentials or experiences.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900">4. Modifications</h2>
          <p>
            We reserve the right to modify or discontinue features of the service at any time without prior notice.
          </p>
        </section>
      </div>
    </div>
  );
};


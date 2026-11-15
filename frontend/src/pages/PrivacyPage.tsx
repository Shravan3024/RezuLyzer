import React from 'react';
import { ShieldCheck, Lock, EyeOff, Trash2, CheckCircle2 } from 'lucide-react';

export const PrivacyPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 mb-3">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Security & Data Integrity</span>
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Privacy Policy</h1>
        <p className="text-sm text-slate-500 mt-1">Last Updated: November 2026</p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-xs space-y-6 text-sm text-slate-700 leading-relaxed">
        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Lock className="w-4 h-4 text-blue-600" />
            1. Document Handling & Processing
          </h2>
          <p>
            ResuLyzer processes uploaded documents (PDF and DOCX) solely for the purpose of extracting resume content,
            evaluating skill alignment, and calculating ATS compatibility metrics requested by you.
          </p>
          <p className="font-semibold text-slate-800">
            We strictly enforce a policy that user resumes are NEVER sold, rented, shared with third parties,
            or used to train public machine learning foundation models.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <EyeOff className="w-4 h-4 text-blue-600" />
            2. Local Execution & Model Privacy
          </h2>
          <p>
            All NLP calculations, including vector embeddings and cosine similarity scoring, execute within our own dedicated
            backend pipeline using local Sentence Transformers and PyMuPDF. We do not dispatch your personal resume text to
            third-party generative chat services or untrusted external endpoints.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Trash2 className="w-4 h-4 text-blue-600" />
            3. Data Retention & Deletion Rights
          </h2>
          <p>
            You retain absolute ownership of all documents. When you delete a resume from the ResuLyzer dashboard,
            the underlying file is immediately removed from private storage and all associated database records are pruned.
          </p>
          <p>
            Guest sessions are tracked with an ephemeral cryptographic identifier and are automatically cleared within 24 hours.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-blue-600" />
            4. Security Measures
          </h2>
          <p>
            ResuLyzer implements industry best practices including file signature magic-byte verification,
            path traversal prevention, bcrypt password hashing, and encrypted JWT tokens.
          </p>
        </section>
      </div>
    </div>
  );
};


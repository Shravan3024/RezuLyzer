import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Shield, Sparkles, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center space-x-2.5">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white">
                <FileText className="w-4 h-4" />
              </div>
              <span className="text-lg font-bold text-slate-900 tracking-tight">
                Resu<span className="text-blue-600">Lyzer</span>
              </span>
            </div>
            <p className="text-sm text-slate-600 max-w-md leading-relaxed">
              Understand Your Resume. Improve Your Opportunities.
              An intelligent NLP platform designed to extract skills, evaluate job requirements, and provide actionable ATS compatibility analysis.
            </p>
            <div className="flex items-center space-x-2 text-xs text-slate-500 pt-2">
              <Shield className="w-4 h-4 text-emerald-600" />
              <span>Private document processing. Your resumes are never sold or used for public model training.</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-3">
              Platform
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/upload" className="text-slate-600 hover:text-blue-600 transition-colors">
                  Resume Upload
                </Link>
              </li>
              <li>
                <Link to="/jobs" className="text-slate-600 hover:text-blue-600 transition-colors">
                  Job Description Analysis
                </Link>
              </li>
              <li>
                <Link to="/compare" className="text-slate-600 hover:text-blue-600 transition-colors">
                  Multi-Role Comparison
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-slate-600 hover:text-blue-600 transition-colors">
                  User Dashboard
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 uppercase tracking-wider mb-3">
              Trust & Security
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/privacy" className="text-slate-600 hover:text-blue-600 transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-slate-600 hover:text-blue-600 transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <span className="text-slate-400">Version 1.0.0 (Production)</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-100 mt-8 pt-8 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500">
          <p>&copy; {new Date().getFullYear()} ResuLyzer. All rights reserved.</p>
          <p className="mt-2 sm:mt-0 flex items-center gap-1">
            Engineered with modern NLP, Transformers & Python FastAPI.
          </p>
        </div>
      </div>
    </footer>
  );
};


import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  FileText,
  LayoutDashboard,
  Upload,
  Briefcase,
  GitCompare,
  User as UserIcon,
  LogOut,
  Sparkles,
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3">
            <Link to="/" className="flex items-center space-x-2.5 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 via-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-sm shadow-blue-500/20 group-hover:scale-105 transition-transform">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <div>
                <span className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-1">
                  Resu<span className="text-blue-600">Lyzer</span>
                  <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                    ATS
                  </span>
                </span>
                <p className="text-[10px] text-slate-500 font-medium hidden sm:block">
                  Intelligent Resume Matching
                </p>
              </div>
            </Link>

            {/* Navigation items */}
            <nav className="hidden md:flex ml-8 space-x-1">
              <Link
                to="/dashboard"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                  isActive('/dashboard')
                    ? 'bg-blue-50 text-blue-700 font-semibold'
                    : 'text-slate-650 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <LayoutDashboard className="w-4 h-4" />
                Dashboard
              </Link>

              <Link
                to="/upload"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                  isActive('/upload')
                    ? 'bg-blue-50 text-blue-700 font-semibold'
                    : 'text-slate-650 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <Upload className="w-4 h-4" />
                Upload Resume
              </Link>

              <Link
                to="/jobs"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                  isActive('/jobs')
                    ? 'bg-blue-50 text-blue-700 font-semibold'
                    : 'text-slate-650 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <Briefcase className="w-4 h-4" />
                Analyze Job
              </Link>

              <Link
                to="/compare"
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                  isActive('/compare')
                    ? 'bg-blue-50 text-blue-700 font-semibold'
                    : 'text-slate-650 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                <GitCompare className="w-4 h-4" />
                Compare Roles
              </Link>
            </nav>
          </div>

          {/* Right side auth & actions */}
          <div className="flex items-center space-x-3">
            {user ? (
              <div className="flex items-center space-x-3">
                <div className="hidden sm:flex flex-col text-right">
                  <span className="text-sm font-medium text-slate-800">{user.name}</span>
                  <span className="text-xs text-slate-500">{user.email}</span>
                </div>
                <div className="w-8 h-8 rounded-full bg-blue-100 border border-blue-200 text-blue-700 flex items-center justify-center font-bold text-xs">
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <button
                  onClick={() => logout()}
                  title="Logout"
                  className="p-2 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-slate-100 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <div className="hidden sm:inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-800 border border-amber-200">
                  Guest Session
                </div>
                <Link
                  to="/login"
                  className="px-3.5 py-2 text-sm font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-xs hover:shadow transition-all"
                >
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};


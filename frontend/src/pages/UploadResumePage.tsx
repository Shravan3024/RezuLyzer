import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  FileText,
  User,
  Mail,
  Phone,
  MapPin,
  Linkedin,
  Github,
  ArrowRight,
  CheckCircle2,
  Edit2,
  Trash2,
  Eye,
  Layers,
  GraduationCap,
  Award,
} from 'lucide-react';
import { resumesApi } from '../services/api';
import { Resume } from '../types';
import { ResumeUploader } from '../components/resume/ResumeUploader';
import { SkillPill } from '../components/analysis/SkillPill';

export const UploadResumePage: React.FC = () => {
  const navigate = useNavigate();
  const [activeResume, setActiveResume] = useState<Resume | null>(null);
  const [showRawText, setShowRawText] = useState(false);
  const [isEditingContact, setIsEditingContact] = useState(false);
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    phone: '',
    location: '',
  });

  // Fetch list of previously uploaded resumes
  const { data: resumesList, refetch: refetchResumes } = useQuery({
    queryKey: ['resumes-list'],
    queryFn: resumesApi.getAll,
  });

  const handleUploadSuccess = (resume: Resume) => {
    setActiveResume(resume);
    refetchResumes();
    if (resume.extracted_data?.candidate_info) {
      const ci = resume.extracted_data.candidate_info;
      setContactForm({
        name: ci.name || '',
        email: ci.email || '',
        phone: ci.phone || '',
        location: ci.location || '',
      });
    }
  };

  const handleSelectExisting = (resume: Resume) => {
    setActiveResume(resume);
    if (resume.extracted_data?.candidate_info) {
      const ci = resume.extracted_data.candidate_info;
      setContactForm({
        name: ci.name || '',
        email: ci.email || '',
        phone: ci.phone || '',
        location: ci.location || '',
      });
    }
  };

  const handleDeleteResume = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this resume?')) {
      await resumesApi.delete(id);
      if (activeResume?.id === id) {
        setActiveResume(null);
      }
      refetchResumes();
    }
  };

  const handleSaveContact = async () => {
    if (!activeResume) return;
    try {
      const updatedData = {
        ...activeResume.extracted_data,
        candidate_info: {
          ...activeResume.extracted_data?.candidate_info,
          ...contactForm,
        },
      };
      const updated = await resumesApi.update(activeResume.id, updatedData);
      setActiveResume(updated);
      setIsEditingContact(false);
    } catch (err) {
      alert('Failed to save updated candidate info');
    }
  };

  const handleProceedToJob = () => {
    if (activeResume) {
      navigate(`/jobs?resume_id=${activeResume.id}`);
    }
  };

  const candidate = activeResume?.extracted_data?.candidate_info;
  const skills = activeResume?.extracted_data?.skills || [];
  const education = activeResume?.extracted_data?.education || [];
  const certifications = activeResume?.extracted_data?.certifications || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Heading */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Upload & Review Resume
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Upload your document in PDF or DOCX format. Our NLP engine will extract contact entities, skills, and sections automatically.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Uploader & Previous Resumes */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
            <h2 className="text-base font-bold text-slate-900">Upload Document</h2>
            <ResumeUploader onUploadSuccess={handleUploadSuccess} selectedResume={activeResume} />
          </div>

          {/* Previous Resumes List */}
          {resumesList && resumesList.length > 0 && (
            <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-900">Your Resumes ({resumesList.length})</h3>
                <span className="text-xs text-slate-400">Click to select</span>
              </div>

              <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
                {resumesList.map((r) => {
                  const isSelected = activeResume?.id === r.id;
                  return (
                    <div
                      key={r.id}
                      onClick={() => handleSelectExisting(r)}
                      className={`p-3 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                        isSelected
                          ? 'border-blue-500 bg-blue-50/60 shadow-2xs'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center space-x-2.5 min-w-0">
                        <FileText
                          className={`w-4 h-4 shrink-0 ${isSelected ? 'text-blue-600' : 'text-slate-400'}`}
                        />
                        <div className="truncate">
                          <p className="text-xs font-semibold text-slate-800 truncate">{r.filename}</p>
                          <p className="text-[10px] text-slate-400">
                            {new Date(r.created_at).toLocaleDateString()} · {r.file_type.toUpperCase()}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center space-x-1">
                        {isSelected && <CheckCircle2 className="w-4 h-4 text-blue-600 shrink-0" />}
                        <button
                          onClick={(e) => handleDeleteResume(r.id, e)}
                          title="Delete Resume"
                          className="p-1 text-slate-400 hover:text-rose-600 rounded transition-colors"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Extracted Information Review */}
        <div className="lg:col-span-2 space-y-6">
          {!activeResume ? (
            <div className="bg-white rounded-2xl border border-slate-200/80 p-12 text-center shadow-xs space-y-3">
              <div className="w-14 h-14 rounded-2xl bg-blue-50 text-blue-500 flex items-center justify-center mx-auto">
                <FileText className="w-7 h-7" />
              </div>
              <h3 className="text-base font-bold text-slate-800">No Resume Selected</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                Upload a new resume or select an existing document from the left panel to review extracted details.
              </p>
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200/80 p-6 sm:p-8 shadow-xs space-y-6">
              {/* Header with action */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-bold text-slate-900">{activeResume.filename}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 font-semibold border border-blue-200">
                      Parsed Successfully
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    Review and verify the extracted entities before matching against job opportunities.
                  </p>
                </div>

                <button
                  onClick={handleProceedToJob}
                  className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm text-white bg-blue-600 hover:bg-blue-700 shadow-sm transition-all"
                >
                  <span>Analyze Against Job</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>

              {/* Candidate Info Card */}
              <div className="bg-slate-50 rounded-xl p-5 border border-slate-200/70 space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs uppercase font-bold text-slate-500 tracking-wider flex items-center gap-1.5">
                    <User className="w-4 h-4 text-blue-600" />
                    Candidate Profile
                  </h3>
                  <button
                    onClick={() => setIsEditingContact(!isEditingContact)}
                    className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
                  >
                    <Edit2 className="w-3 h-3" />
                    {isEditingContact ? 'Cancel' : 'Edit Info'}
                  </button>
                </div>

                {isEditingContact ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                    <div>
                      <label className="text-[11px] font-semibold text-slate-600">Full Name</label>
                      <input
                        type="text"
                        value={contactForm.name}
                        onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                        className="mt-1 w-full px-3 py-1.5 rounded-lg border border-slate-300 text-xs focus:ring-2 focus:ring-blue-500 outline-hidden"
                      />
                    </div>
                    <div>
                      <label className="text-[11px] font-semibold text-slate-600">Email Address</label>
                      <input
                        type="email"
                        value={contactForm.email}
                        onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                        className="mt-1 w-full px-3 py-1.5 rounded-lg border border-slate-300 text-xs focus:ring-2 focus:ring-blue-500 outline-hidden"
                      />
                    </div>
                    <div>
                      <label className="text-[11px] font-semibold text-slate-600">Phone</label>
                      <input
                        type="text"
                        value={contactForm.phone}
                        onChange={(e) => setContactForm({ ...contactForm, phone: e.target.value })}
                        className="mt-1 w-full px-3 py-1.5 rounded-lg border border-slate-300 text-xs focus:ring-2 focus:ring-blue-500 outline-hidden"
                      />
                    </div>
                    <div>
                      <label className="text-[11px] font-semibold text-slate-600">Location</label>
                      <input
                        type="text"
                        value={contactForm.location}
                        onChange={(e) => setContactForm({ ...contactForm, location: e.target.value })}
                        className="mt-1 w-full px-3 py-1.5 rounded-lg border border-slate-300 text-xs focus:ring-2 focus:ring-blue-500 outline-hidden"
                      />
                    </div>
                    <div className="sm:col-span-2 flex justify-end gap-2 pt-2">
                      <button
                        onClick={handleSaveContact}
                        className="px-4 py-1.5 bg-blue-600 text-white rounded-lg text-xs font-semibold hover:bg-blue-700"
                      >
                        Save Changes
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div className="flex items-center gap-2 text-slate-700">
                      <User className="w-3.5 h-3.5 text-slate-400" />
                      <span className="font-semibold">{candidate?.name || 'Name not detected'}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-700">
                      <Mail className="w-3.5 h-3.5 text-slate-400" />
                      <span>{candidate?.email || 'Email not detected'}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-700">
                      <Phone className="w-3.5 h-3.5 text-slate-400" />
                      <span>{candidate?.phone || 'Phone not detected'}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-700">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      <span>{candidate?.location || 'Location not specified'}</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Skills Section */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs uppercase font-bold text-slate-500 tracking-wider flex items-center gap-1.5">
                    <Layers className="w-4 h-4 text-blue-600" />
                    Detected Skills ({skills.length})
                  </h3>
                </div>

                {skills.length === 0 ? (
                  <p className="text-xs text-slate-400">No skills identified in the taxonomy.</p>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {skills.map((s, idx) => (
                      <SkillPill
                        key={`${s.name}-${idx}`}
                        name={s.name}
                        category={s.category}
                        type="matched"
                        matchedAs={s.matched_as}
                      />
                    ))}
                  </div>
                )}
              </div>

              {/* Education Section */}
              {education.length > 0 && (
                <div className="space-y-3 pt-2">
                  <h3 className="text-xs uppercase font-bold text-slate-500 tracking-wider flex items-center gap-1.5">
                    <GraduationCap className="w-4 h-4 text-blue-600" />
                    Education
                  </h3>
                  <div className="space-y-2">
                    {education.map((edu, i) => (
                      <div key={i} className="p-3 rounded-lg bg-slate-50 border border-slate-200/60 text-xs">
                        <p className="font-semibold text-slate-800">{edu.text}</p>
                        {edu.degree_level && (
                          <span className="inline-block mt-1 px-2 py-0.5 rounded bg-blue-100 text-blue-800 text-[10px] font-bold uppercase">
                            Tier: {edu.degree_level}
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Certifications Section */}
              {certifications.length > 0 && (
                <div className="space-y-3 pt-2">
                  <h3 className="text-xs uppercase font-bold text-slate-500 tracking-wider flex items-center gap-1.5">
                    <Award className="w-4 h-4 text-blue-600" />
                    Certifications
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {certifications.map((c, i) => (
                      <span key={i} className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-medium">
                        {c}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Raw Text Toggle */}
              <div className="pt-4 border-t border-slate-100">
                <button
                  onClick={() => setShowRawText(!showRawText)}
                  className="text-xs font-semibold text-slate-600 hover:text-slate-900 flex items-center gap-1"
                >
                  <Eye className="w-3.5 h-3.5" />
                  {showRawText ? 'Hide Raw Extracted Text' : 'View Full Extracted Text'}
                </button>

                {showRawText && (
                  <pre className="mt-3 p-4 bg-slate-900 text-slate-200 rounded-xl text-[11px] leading-relaxed max-h-64 overflow-y-auto font-mono whitespace-pre-wrap">
                    {activeResume.extracted_text}
                  </pre>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

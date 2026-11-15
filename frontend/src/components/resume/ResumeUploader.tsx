import React, { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { Upload, FileText, CheckCircle2, AlertTriangle, Loader2, ArrowRight } from 'lucide-react';
import { resumesApi } from '../../services/api';
import { Resume } from '../../types';

interface ResumeUploaderProps {
  onUploadSuccess: (resume: Resume) => void;
  selectedResume?: Resume | null;
}

export const ResumeUploader: React.FC<ResumeUploaderProps> = ({
  onUploadSuccess,
  selectedResume,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedResume, setUploadedResume] = useState<Resume | null>(selectedResume || null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const validateFile = (file: File): string | null => {
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (ext !== '.pdf' && ext !== '.docx') {
      return 'Unsupported format. Please upload a PDF or DOCX resume.';
    }
    const maxMb = 10;
    if (file.size > maxMb * 1024 * 1024) {
      return `File size exceeds ${maxMb}MB limit.`;
    }
    if (file.size === 0) {
      return 'The selected file is empty.';
    }
    return null;
  };

  const processUpload = async (file: File) => {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError(null);
    setIsUploading(true);

    try {
      const response = await resumesApi.upload(file);
      setUploadedResume(response);
      onUploadSuccess(response);
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to upload and parse resume. Please check file format.';
      setError(msg);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      processUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      processUpload(e.target.files[0]);
    }
  };

  return (
    <div className="space-y-4">
      {/* Upload Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isUploading && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer ${
          isDragging
            ? 'border-blue-500 bg-blue-50/70 scale-[1.01]'
            : 'border-slate-300 hover:border-blue-400 bg-white hover:bg-slate-50/60'
        } ${isUploading ? 'opacity-70 pointer-events-none' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          onChange={handleFileInputChange}
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="w-14 h-14 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-100 shadow-2xs">
            {isUploading ? (
              <Loader2 className="w-7 h-7 animate-spin text-blue-600" />
            ) : (
              <Upload className="w-7 h-7 text-blue-600" />
            )}
          </div>

          <div>
            <h4 className="text-base font-semibold text-slate-800">
              {isUploading ? 'Processing & Parsing Document...' : 'Upload your resume'}
            </h4>
            <p className="text-sm text-slate-500 mt-1">
              Drag & drop your file here, or{' '}
              <span className="text-blue-600 font-semibold underline underline-offset-2">
                browse files
              </span>
            </p>
          </div>

          <div className="flex items-center space-x-3 text-xs text-slate-400 pt-2">
            <span className="px-2 py-0.5 rounded-md bg-slate-100 font-medium text-slate-600">PDF</span>
            <span className="px-2 py-0.5 rounded-md bg-slate-100 font-medium text-slate-600">DOCX</span>
            <span>Up to 10MB</span>
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="flex items-start space-x-3 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm">
          <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold">Upload Failed</p>
            <p className="text-xs text-rose-700 mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Success / Current Resume Card */}
      {uploadedResume && !error && (
        <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-bold text-slate-900">{uploadedResume.filename}</span>
                <span className="text-[10px] uppercase font-bold px-1.5 py-0.2 rounded bg-emerald-100 text-emerald-800">
                  {uploadedResume.file_type}
                </span>
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                {uploadedResume.extracted_data?.candidate_info?.name
                  ? `Candidate: ${uploadedResume.extracted_data.candidate_info.name} · `
                  : ''}
                {uploadedResume.extracted_data?.total_skills_detected || 0} skills detected ·{' '}
                {uploadedResume.extracted_data?.word_count || 0} words
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 text-emerald-700 text-xs font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>Ready for Analysis</span>
          </div>
        </div>
      )}
    </div>
  );
};


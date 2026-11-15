export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface CandidateInfo {
  name?: string | null;
  email?: string | null;
  phone?: string | null;
  location?: string | null;
  linkedin?: string | null;
  github?: string | null;
}

export interface SkillItem {
  name: string;
  category: string;
  matched_as?: string;
  type?: 'required' | 'preferred';
  skill?: string;
}

export interface Resume {
  id: string;
  filename: string;
  file_type: string;
  user_id?: string | null;
  created_at: string;
  extracted_data?: {
    candidate_info?: CandidateInfo;
    sections_present?: string[];
    skills?: SkillItem[];
    skill_names?: string[];
    education?: any[];
    certifications?: string[];
    has_summary?: boolean;
    has_experience?: boolean;
    has_education?: boolean;
    has_skills_section?: boolean;
    has_projects_section?: boolean;
    total_skills_detected?: number;
    char_count?: number;
    word_count?: number;
    metadata?: {
      format: string;
      page_count?: number;
      image_count?: number;
      paragraph_count?: number;
      table_count?: number;
      word_count?: number;
      character_count?: number;
    };
  };
  extracted_text?: string;
}

export interface JobTemplate {
  id: number;
  role_name: string;
  category: string;
  description: string;
  requirements: {
    role_name: string;
    category: string;
    description: string;
    required_skills: string[];
    preferred_skills: string[];
    min_experience_years: number;
    required_education: string[];
    responsibilities?: string[];
  };
  is_active: boolean;
}

export interface JobDescription {
  id: string;
  job_title: string;
  company_name?: string | null;
  description: string;
  extracted_requirements?: {
    job_title: string;
    required_skills: string[];
    preferred_skills: string[];
    all_skills: string[];
    min_experience_years: number;
    education_level: string;
    keywords: { keyword: string; frequency: number }[];
    raw_text_length: number;
    word_count: number;
  };
  source_type: string;
  created_at: string;
}

export interface ScoreComponent {
  score: number;
  weight: number;
  weighted_contribution: number;
  label: string;
}

export interface ScoreBreakdown {
  required_skills: ScoreComponent;
  semantic_similarity: ScoreComponent;
  keyword_relevance: ScoreComponent;
  experience_relevance: ScoreComponent;
  education_relevance: ScoreComponent;
  resume_structure: ScoreComponent;
}

export interface MissingSkills {
  required: string[];
  preferred: string[];
}

export interface KeywordAnalysis {
  matched_keywords: { keyword: string; frequency_in_resume: number; frequency_in_job: number }[];
  missing_keywords: string[];
  matched_count: number;
  total_job_keywords: number;
  keyword_coverage_pct: number;
}

export interface Recommendation {
  type: string;
  priority: 'high' | 'medium' | 'low';
  title: string;
  description: string;
  action: string;
}

export interface AnalysisResult {
  id: string;
  resume_id: string;
  job_description_id: string;
  user_id?: string | null;
  ats_score: number;
  score_breakdown: ScoreBreakdown;
  matched_skills: SkillItem[];
  missing_skills: MissingSkills;
  keyword_analysis: KeywordAnalysis;
  semantic_similarity: number;
  experience_analysis: {
    score: number;
    candidate_years?: number | null;
    required_years: number;
    status: string;
    explanation: string;
  };
  education_analysis: {
    score: number;
    candidate_highest_level: string;
    required_level: string;
    status: string;
    explanation: string;
  };
  structure_analysis: {
    score: number;
    contact_score: number;
    section_score: number;
    word_count: number;
    has_contact_info: boolean;
    has_summary: boolean;
    has_skills: boolean;
    has_experience: boolean;
    has_education: boolean;
    has_projects: boolean;
  };
  recommendations: Recommendation[];
  processing_status: string;
  error_message?: string | null;
  created_at: string;
  resume_filename?: string;
  job_title?: string;
  company_name?: string | null;
}

export interface JobComparisonItem {
  analysis_id: string;
  job_description_id: string;
  job_title: string;
  company_name?: string | null;
  ats_score: number;
  score_category: string;
  required_skills_coverage: number;
  semantic_similarity: number;
  matched_skills_count: number;
  missing_skills_count: number;
  missing_required_skills: string[];
  experience_match: string;
  created_at: string;
}

export interface MultiJobCompareResponse {
  resume_id: string;
  resume_filename: string;
  candidate_name?: string | null;
  total_compared: number;
  comparisons: JobComparisonItem[];
}

export interface RecentActivityItem {
  analysis_id: string;
  resume_id: string;
  resume_filename: string;
  job_title: string;
  company_name?: string | null;
  ats_score: number;
  score_category: string;
  created_at: string;
}

export interface DashboardStats {
  total_resumes: number;
  total_analyses: number;
  highest_ats_score: number;
  average_ats_score: number;
  recent_roles_analyzed: string[];
  recent_activity: RecentActivityItem[];
}

import axios from 'axios';
import {
  AuthResponse,
  User,
  Resume,
  JobTemplate,
  JobDescription,
  AnalysisResult,
  DashboardStats,
  RecentActivityItem,
  MultiJobCompareResponse,
} from '../types';

export const API_BASE = (import.meta as any).env?.VITE_API_URL || '/api/v1';

// Initialize or retrieve guest session id
export const getOrCreateGuestSessionId = (): string => {
  let sessionId = localStorage.getItem('guest_session_id');
  if (!sessionId) {
    sessionId = 'guest_' + Math.random().toString(36).substring(2, 12) + Date.now().toString(36);
    localStorage.setItem('guest_session_id', sessionId);
  }
  return sessionId;
};

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach auth token and guest session ID
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers['X-Guest-Session-ID'] = getOrCreateGuestSessionId();
  return config;
});

// Response interceptor: handle 401 unauthorized
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if invalid
      if (localStorage.getItem('token')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    return Promise.reject(error);
  }
);

// Auth Service
export const authApi = {
  register: async (data: { name: string; email: string; password: string }): Promise<AuthResponse> => {
    const res = await apiClient.post<AuthResponse>('/auth/register', data);
    return res.data;
  },
  login: async (data: { email: string; password: string }): Promise<AuthResponse> => {
    const res = await apiClient.post<AuthResponse>('/auth/login', data);
    return res.data;
  },
  getMe: async (): Promise<User> => {
    const res = await apiClient.get<User>('/auth/me');
    return res.data;
  },
  logout: async () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    await apiClient.post('/auth/logout');
  },
};

// Resumes Service
export const resumesApi = {
  upload: async (file: File): Promise<Resume> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<Resume>('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },
  getAll: async (): Promise<Resume[]> => {
    const res = await apiClient.get<Resume[]>('/resumes/');
    return res.data;
  },
  getById: async (id: string): Promise<Resume> => {
    const res = await apiClient.get<Resume>(`/resumes/${id}`);
    return res.data;
  },
  update: async (id: string, extracted_data: any): Promise<Resume> => {
    const res = await apiClient.put<Resume>(`/resumes/${id}`, { extracted_data });
    return res.data;
  },
  delete: async (id: string): Promise<{ message: string }> => {
    const res = await apiClient.delete<{ message: string }>(`/resumes/${id}`);
    return res.data;
  },
  reprocess: async (id: string): Promise<Resume> => {
    const res = await apiClient.post<Resume>(`/resumes/${id}/reprocess`);
    return res.data;
  },
};

// Jobs Service
export const jobsApi = {
  analyze: async (data: {
    job_title: string;
    description: string;
    company_name?: string;
    custom_requirements?: any;
  }) => {
    const res = await apiClient.post('/jobs/analyze', data);
    return res.data;
  },
  getTemplates: async (): Promise<JobTemplate[]> => {
    const res = await apiClient.get<JobTemplate[]>('/jobs/templates');
    return res.data;
  },
  getTemplateByRole: async (roleName: string): Promise<JobTemplate> => {
    const res = await apiClient.get<JobTemplate>(`/jobs/templates/${encodeURIComponent(roleName)}`);
    return res.data;
  },
  create: async (data: {
    job_title: string;
    description: string;
    company_name?: string;
    source_type?: string;
    custom_requirements?: any;
  }): Promise<JobDescription> => {
    const res = await apiClient.post<JobDescription>('/jobs/', data);
    return res.data;
  },
  getHistory: async (): Promise<JobDescription[]> => {
    const res = await apiClient.get<JobDescription[]>('/jobs/history');
    return res.data;
  },
};

// Analysis Service
export const analysisApi = {
  analyze: async (data: {
    resume_id: string;
    job_description_id?: string;
    job_title?: string;
    company_name?: string;
    job_description_text?: string;
    source_type?: string;
    template_role_name?: string;
    custom_requirements?: any;
  }): Promise<AnalysisResult> => {
    const res = await apiClient.post<AnalysisResult>('/analysis/', data);
    return res.data;
  },
  getById: async (id: string): Promise<AnalysisResult> => {
    const res = await apiClient.get<AnalysisResult>(`/analysis/${id}`);
    return res.data;
  },
  getHistory: async (): Promise<AnalysisResult[]> => {
    const res = await apiClient.get<AnalysisResult[]>('/analysis/history');
    return res.data;
  },
  delete: async (id: string): Promise<{ message: string }> => {
    const res = await apiClient.delete<{ message: string }>(`/analysis/${id}`);
    return res.data;
  },
  getReportUrl: (id: string): string => {
    return `${API_BASE}/analysis/${id}/report`;
  },
  downloadReport: async (id: string, filename: string) => {
    const res = await apiClient.get(`/analysis/${id}/report`, {
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename || `ResuLyzer_Audit_${id.substring(0, 8)}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },
  compareMultipleJobs: async (data: {
    resume_id: string;
    job_description_ids?: string[];
    analysis_ids?: string[];
  }): Promise<MultiJobCompareResponse> => {
    const res = await apiClient.post<MultiJobCompareResponse>('/analysis/compare', data);
    return res.data;
  },
};

// Dashboard Service
export const dashboardApi = {
  getStats: async (): Promise<DashboardStats> => {
    const res = await apiClient.get<DashboardStats>('/dashboard/stats');
    return res.data;
  },
  getRecentActivity: async (): Promise<RecentActivityItem[]> => {
    const res = await apiClient.get<RecentActivityItem[]>('/dashboard/recent-activity');
    return res.data;
  },
};

export default apiClient;


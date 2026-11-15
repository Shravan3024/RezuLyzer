from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AnalysisCreateRequest(BaseModel):
    resume_id: str
    job_description_id: Optional[str] = None
    # Or allow inline job description submission
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    job_description_text: Optional[str] = None
    source_type: Optional[str] = "pasted"  # pasted, template, role_generated
    template_role_name: Optional[str] = None
    custom_requirements: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    id: str
    resume_id: str
    job_description_id: str
    user_id: Optional[str] = None
    ats_score: float
    score_breakdown: Dict[str, Any]
    matched_skills: List[Dict[str, Any]]
    missing_skills: Dict[str, Any]
    keyword_analysis: Dict[str, Any]
    semantic_similarity: float
    experience_analysis: Dict[str, Any]
    education_analysis: Dict[str, Any]
    structure_analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    processing_status: str
    error_message: Optional[str] = None
    created_at: datetime
    # Metadata for UI
    resume_filename: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True

class MultiJobCompareRequest(BaseModel):
    resume_id: str
    job_description_ids: Optional[List[str]] = None
    # Or direct analysis IDs
    analysis_ids: Optional[List[str]] = None

class JobComparisonItem(BaseModel):
    analysis_id: str
    job_description_id: str
    job_title: str
    company_name: Optional[str] = None
    ats_score: float
    score_category: str
    required_skills_coverage: float
    semantic_similarity: float
    matched_skills_count: int
    missing_skills_count: int
    missing_required_skills: List[str]
    experience_match: str
    created_at: datetime

class MultiJobCompareResponse(BaseModel):
    resume_id: str
    resume_filename: str
    candidate_name: Optional[str] = None
    total_compared: int
    comparisons: List[JobComparisonItem]


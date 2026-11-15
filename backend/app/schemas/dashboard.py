from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class RecentActivityItem(BaseModel):
    analysis_id: str
    resume_id: str
    resume_filename: str
    job_title: str
    company_name: Optional[str] = None
    ats_score: float
    score_category: str
    created_at: datetime

class DashboardStatsResponse(BaseModel):
    total_resumes: int
    total_analyses: int
    highest_ats_score: float
    average_ats_score: float
    recent_roles_analyzed: List[str]
    recent_activity: List[RecentActivityItem]


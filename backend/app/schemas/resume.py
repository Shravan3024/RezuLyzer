from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class ResumeCandidateInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class ResumeUpdate(BaseModel):
    extracted_data: Optional[Dict[str, Any]] = None

class ResumeResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    user_id: Optional[str] = None
    created_at: datetime
    extracted_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class ResumeDetailResponse(ResumeResponse):
    extracted_text: str


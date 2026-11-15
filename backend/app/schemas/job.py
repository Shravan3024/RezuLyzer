from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class JobDescriptionCreate(BaseModel):
    job_title: str = Field(..., min_length=2, max_length=200)
    company_name: Optional[str] = None
    description: str = Field(..., min_length=10)
    source_type: Optional[str] = "pasted"
    custom_requirements: Optional[Dict[str, Any]] = None

class JobRoleAnalyzeRequest(BaseModel):
    role_name: str
    custom_modifications: Optional[Dict[str, Any]] = None

class JobTemplateResponse(BaseModel):
    id: int
    role_name: str
    category: str
    description: str
    requirements: Dict[str, Any]
    is_active: bool

    class Config:
        from_attributes = True

class JobDescriptionResponse(BaseModel):
    id: str
    job_title: str
    company_name: Optional[str] = None
    description: str
    extracted_requirements: Optional[Dict[str, Any]] = None
    source_type: str
    created_at: datetime

    class Config:
        from_attributes = True


from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_current_user, get_session_id
from app.models.user import User
from app.models.job import JobDescription
from app.schemas.job import (
    JobDescriptionCreate,
    JobDescriptionResponse,
    JobTemplateResponse,
    JobRoleAnalyzeRequest
)
from app.services.job_analyzer import job_analyzer

router = APIRouter()

@router.post("/analyze", response_model=Dict[str, Any])
def analyze_job_text(request: JobDescriptionCreate):
    """
    Analyzes job description text and extracts requirements without persisting yet.
    Allows candidate to review and customize required/preferred skills.
    """
    analysis = job_analyzer.analyze_job_description(
        job_title=request.job_title,
        description_text=request.description,
        custom_requirements=request.custom_requirements
    )
    return analysis

@router.get("/templates", response_model=List[Dict[str, Any]])
def get_job_templates():
    """
    Returns all preconfigured job role templates across tech and non-tech industries.
    """
    return job_analyzer.get_all_templates()

@router.get("/templates/{role_name}", response_model=Dict[str, Any])
def get_job_template_by_role(role_name: str):
    template = job_analyzer.get_template(role_name)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template for role '{role_name}' not found."
        )
    return template

@router.post("/", response_model=JobDescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_job_description(
    job_in: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    # Extract requirements
    extracted = job_analyzer.analyze_job_description(
        job_title=job_in.job_title,
        description_text=job_in.description,
        custom_requirements=job_in.custom_requirements
    )

    user_id = current_user.id if current_user else None

    job_record = JobDescription(
        user_id=user_id,
        guest_session_id=session_id if not user_id else None,
        job_title=job_in.job_title,
        company_name=job_in.company_name,
        description=job_in.description,
        extracted_requirements=extracted,
        source_type=job_in.source_type or "pasted"
    )
    db.add(job_record)
    db.commit()
    db.refresh(job_record)
    return job_record

@router.get("/history", response_model=List[JobDescriptionResponse])
def get_job_history(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session_id: str = Depends(get_session_id)
):
    query = db.query(JobDescription)
    if current_user:
        query = query.filter(JobDescription.user_id == current_user.id)
    else:
        query = query.filter(JobDescription.guest_session_id == session_id)
    return query.order_by(JobDescription.created_at.desc()).all()

